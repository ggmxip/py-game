import socket
import threading
import random
import json
import time

HOST = "0.0.0.0"
PORT = 5555

QUESTIONS = [
    ("What is 2 + 2?", "4"),
    ("What is the capital of Japan?", "tokyo"),
    ("What color is the sky on a clear day?", "blue"),
    ("How many legs does a cat have?", "4"),
    ("What planet is known as the Red Planet?", "mars"),
    ("What is 10 * 10?", "100"),
    ("What is the opposite of hot?", "cold"),
    ("What sound does a dog make?", "bark"),
]


class QuizServer:
    def __init__(self):
        self.clients = []
        self.scores = {}

    def handle_client(self, conn, addr, player_id):
        print(f"[NEW] Player {player_id} connected from {addr}")
        conn.send(json.dumps({"type": "welcome", "player_id": player_id}).encode())

        for q_text, q_answer in QUESTIONS:
            conn.send(json.dumps({"type": "question", "q": q_text}).encode())
            try:
                data = conn.recv(1024).decode().strip().lower()
                correct = data == q_answer
                if correct:
                    self.scores[player_id] = self.scores.get(player_id, 0) + 1
                    conn.send(json.dumps({"type": "result", "correct": True}).encode())
                else:
                    conn.send(json.dumps({"type": "result", "correct": False, "answer": q_answer}).encode())
            except:
                break

        final_score = self.scores.get(player_id, 0)
        conn.send(json.dumps({"type": "final", "score": final_score, "total": len(QUESTIONS)}).encode())
        conn.close()
        print(f"[LEFT] Player {player_id} (score: {final_score}/{len(QUESTIONS)})")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")
        player_id = 1
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr, player_id))
            thread.daemon = True
            thread.start()
            player_id += 1


if __name__ == "__main__":
    QuizServer().start()