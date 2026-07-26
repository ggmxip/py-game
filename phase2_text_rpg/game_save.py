import json
import os

SAVE_FILE = "save_data.json"


def save_game(player, current_room):
    data = {
        "name": player.name,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "attack": player.attack,
        "defense": player.defense,
        "gold": player.gold,
        "inventory": player.inventory,
        "room": current_room,
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("Game saved!")
    except OSError:
        print("Save failed!")


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def has_save():
    return os.path.exists(SAVE_FILE)


def delete_save():
    if has_save():
        os.remove(SAVE_FILE)