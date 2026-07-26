import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5555


def main():
    print("=== QUIZ BATTLE CLIENT ===")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}\n")

    while True:
        try:
            data = sock.recv(4096).decode()
            if not data:
                break
            msg = json.loads(data)

            if msg["type"] == "welcome":
                print(f"You are Player {msg['player_id']}!")
                print("Answer all questions to get your score.\n")

            elif msg["type"] == "question":
                print(f"Q: {msg['q']}")
                answer = input("> ")
                sock.send(answer.encode())

            elif msg["type"] == "result":
                if msg["correct"]:
                    print("Correct!\n")
                else:
                    print(f"Wrong! The answer was: {msg['answer']}\n")

            elif msg["type"] == "final":
                print(f"\n=== GAME OVER ===")
                print(f"Final Score: {msg['score']}/{msg['total']}")
                break
        except:
            break

    sock.close()


if __name__ == "__main__":
    main()