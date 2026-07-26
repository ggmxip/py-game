import json
import os

HIGHSCORES_FILE = "highscores.json"


def load_highscores():
    if not os.path.exists(HIGHSCORES_FILE):
        return []
    try:
        with open(HIGHSCORES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_highscores(scores):
    try:
        with open(HIGHSCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        print("Could not save high scores.")


def is_highscore(score, scores, top_n=5):
    if len(scores) < top_n:
        return True
    return score > scores[-1]["score"]


def add_score(name, score, difficulty, scores, top_n=5):
    scores.append({"name": name, "score": score, "difficulty": difficulty})
    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores[:top_n]


def display_highscores(scores):
    if not scores:
        print("\n  No high scores yet!")
        return
    print("\n  HIGH SCORES")
    print("  " + "-" * 30)
    for i, entry in enumerate(scores, 1):
        print(f"  {i}. {entry['name']} - {entry['score']}/10 ({entry['difficulty']})")
    print()