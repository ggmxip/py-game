from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import random
import json
import sqlite3
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

DB_FILE = "quiz.db"

QUESTIONS = [
    ("What is 2 + 2?", "4"),
    ("What is the capital of France?", "paris"),
    ("How many continents are there?", "7"),
    ("What color do you get mixing red and blue?", "purple"),
    ("What planet is closest to the sun?", "mercury"),
    ("What is 15 * 3?", "45"),
    ("What is the largest ocean?", "pacific"),
    ("What gas do plants absorb?", "carbon dioxide"),
]


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, score INTEGER, total INTEGER)")
    conn.commit()
    conn.close()


def save_score(name, score, total):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score, total) VALUES (?, ?, ?)", (name, score, total))
    conn.commit()
    conn.close()


def get_top_scores(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, score, total FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "score": r[1], "total": r[2]} for r in rows]


init_db()


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())


@app.get("/scores")
async def get_scores():
    return get_top_scores()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    random.shuffle(QUESTIONS)
    score = 0
    name = ""

    try:
        data = await websocket.receive_text()
        msg = json.loads(data)
        name = msg.get("name", "Anonymous")

        await websocket.send_text(json.dumps({"type": "start", "total": len(QUESTIONS)}))

        for q_text, q_answer in QUESTIONS:
            await websocket.send_text(json.dumps({"type": "question", "q": q_text}))
            resp = await websocket.receive_text()
            resp_data = json.loads(resp)

            if resp_data.get("answer", "").strip().lower() == q_answer:
                score += 1
                await websocket.send_text(json.dumps({"type": "result", "correct": True}))
            else:
                await websocket.send_text(json.dumps({"type": "result", "correct": False, "answer": q_answer}))

        save_score(name, score, len(QUESTIONS))
        await websocket.send_text(json.dumps({
            "type": "final", "score": score, "total": len(QUESTIONS), "name": name
        }))

    except WebSocketDisconnect:
        pass