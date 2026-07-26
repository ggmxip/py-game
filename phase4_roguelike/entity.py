class Entity:
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy, game_map):
        nx, ny = self.x + dx, self.y + dy
        w, h = len(game_map[0]), len(game_map)
        if 0 <= nx < w and 0 <= ny < h and not game_map[ny][nx].blocked:
            self.x, self.y = nx, ny
            return True
        return False


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "@", (255, 255, 255), "Player", blocks=True)
        self.hp = 30
        self.max_hp = 30
        self.attack = 5
        self.defense = 2
        self.fov_radius = 8

    def distance_to(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))


class Enemy(Entity):
    def __init__(self, x, y, name, char, hp, attack, defense, xp):
        super().__init__(x, y, char, (255, 0, 0), name, blocks=True)
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.xp = xp

    def take_damage(self, amount):
        dmg = max(1, amount - self.defense)
        self.hp -= dmg
        return dmg