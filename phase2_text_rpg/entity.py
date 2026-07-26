from dataclasses import dataclass


@dataclass
class Entity:
    name: str
    hp: int
    max_hp: int
    attack: int
    defense: int

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage = max(1, amount - self.defense)
        self.hp -= damage
        return damage


class Player(Entity):
    def __init__(self, name):
        super().__init__(name, hp=30, max_hp=30, attack=8, defense=2)
        self.inventory = []
        self.gold = 0

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)


class Enemy(Entity):
    def __init__(self, name, hp, attack, defense, xp_reward, gold_reward):
        super().__init__(name, hp, hp, attack, defense)
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward