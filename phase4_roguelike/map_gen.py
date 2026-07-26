import random


class Tile:
    def __init__(self, blocked):
        self.blocked = blocked
        self.explored = False


def generate_dungeon(w, h, room_min=4, room_max=10, max_rooms=10):
    tiles = [[Tile(True) for _ in range(w)] for _ in range(h)]
    rooms = []

    for _ in range(max_rooms):
        rw = random.randint(room_min, room_max)
        rh = random.randint(room_min, room_max)
        rx = random.randint(1, w - rw - 1)
        ry = random.randint(1, h - rh - 1)

        room = (rx, ry, rw, rh)
        overlaps = False
        for other in rooms:
            if rects_overlap(room, other):
                overlaps = True
                break
        if overlaps:
            continue

        for y in range(ry, ry + rh):
            for x in range(rx, rx + rw):
                tiles[y][x] = Tile(False)
        rooms.append(room)

    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i][0] + rooms[i][2] // 2, rooms[i][1] + rooms[i][3] // 2
        x2, y2 = rooms[i + 1][0] + rooms[i + 1][2] // 2, rooms[i + 1][1] + rooms[i + 1][3] // 2
        carve_h_tunnel(tiles, x1, x2, y1)
        carve_v_tunnel(tiles, y1, y2, x2)

    return tiles, rooms


def rects_overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw + 1 and ax + aw + 1 > bx and ay < by + bh + 1 and ay + ah + 1 > by


def carve_h_tunnel(tiles, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
            tiles[y][x] = Tile(False)


def carve_v_tunnel(tiles, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
            tiles[y][x] = Tile(False)


def place_entities(rooms, player, num_enemies=6):
    enemies = []
    placed = 0
    for room in rooms[1:]:
        rx, ry, rw, rh = room
        cx, cy = rx + rw // 2, ry + rh // 2
        if placed < num_enemies and random.random() < 0.6:
            from entity import Enemy
            e = Enemy(cx, cy, "Goblin", "g", hp=8, attack=3, defense=1, xp=10)
            enemies.append(e)
            placed += 1
    player.x, player.y = rooms[0][0] + rooms[0][2] // 2, rooms[0][1] + rooms[0][3] // 2
    return enemies