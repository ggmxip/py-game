from dataclasses import dataclass, field


@dataclass
class Room:
    name: str
    description: str
    exits: dict = field(default_factory=dict)
    enemies: list = field(default_factory=list)
    items: list = field(default_factory=list)
    visited: bool = False


WORLD = {
    "town": Room(
        "Town Square", "A peaceful village square with a fountain.",
        exits={"north": "forest", "east": "shop", "south": "cave"},
    ),
    "shop": Room(
        "Item Shop", "A dusty shop with potions on the shelves.",
        exits={"west": "town"},
        items=["health_potion", "rusty_sword"],
    ),
    "forest": Room(
        "Dark Forest", "Thick trees block the sunlight.",
        exits={"south": "town", "east": "clearing"},
        enemies=["goblin", "wolf"],
    ),
    "clearing": Room(
        "Forest Clearing", "Sunlight breaks through the canopy.",
        exits={"west": "forest", "north": "lake"},
        enemies=["wolf"],
        items=["health_potion"],
    ),
    "lake": Room(
        "Mystic Lake", "The water glows faintly blue.",
        exits={"south": "clearing"},
        items=["iron_sword", "big_potion"],
    ),
    "cave": Room(
        "Dark Cave", "It's damp and cold. Something stirs ahead.",
        exits={"north": "town"},
        enemies={"easy": ["goblin", "giant_rat"], "boss": ["troll"]},
    ),
}

ENEMY_TEMPLATES = {
    "goblin": {"hp": 10, "attack": 5, "defense": 1, "xp": 10, "gold": 5},
    "wolf": {"hp": 15, "attack": 7, "defense": 2, "xp": 15, "gold": 8},
    "giant_rat": {"hp": 8, "attack": 4, "defense": 0, "xp": 8, "gold": 3},
    "troll": {"hp": 40, "attack": 12, "defense": 4, "xp": 50, "gold": 30},
}


def get_room(room_id):
    import copy
    room = WORLD.get(room_id)
    if room is None:
        return None
    room_copy = copy.copy(room)
    enemies = []
    for e in room.enemies:
        if isinstance(room.enemies, dict):
            for group in room.enemies.values():
                for eid in group:
                    if eid in ENEMY_TEMPLATES:
                        enemies.append(eid)
        elif e in ENEMY_TEMPLATES:
            enemies.append(e)
    room_copy.enemies = enemies
    return room_copy