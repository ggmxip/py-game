from dataclasses import dataclass


@dataclass
class Item:
    name: str
    description: str


@dataclass
class Weapon(Item):
    attack_bonus: int = 0


@dataclass
class Potion(Item):
    heal_amount: int = 10


ITEMS = {
    "rusty_sword": Weapon("Rusty Sword", "A worn blade", attack_bonus=3),
    "iron_sword": Weapon("Iron Sword", "A sturdy blade", attack_bonus=6),
    "steel_sword": Weapon("Steel Sword", "A fine blade", attack_bonus=10),
    "health_potion": Potion("Health Potion", "Restores 15 HP", heal_amount=15),
    "big_potion": Potion("Big Potion", "Restores 30 HP", heal_amount=30),
    "leather_armor": Item("Leather Armor", "Basic protection (def+2)"),
    "chainmail": Item("Chainmail", "Strong protection (def+5)"),
}


def get_item(item_id):
    return ITEMS.get(item_id)