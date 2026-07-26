import math

TILE_WALL = 0
TILE_FLOOR = 1


def calculate_fov(start_x, start_y, radius, game_map):
    w, h = len(game_map[0]), len(game_map)
    visible = set()
    visible.add((start_x, start_y))

    for angle in range(0, 360, 2):
        rad = math.radians(angle)
        for dist in range(1, radius + 1):
            x = start_x + round(math.cos(rad) * dist)
            y = start_y + round(math.sin(rad) * dist)
            if 0 <= x < w and 0 <= y < h:
                visible.add((x, y))
                if game_map[y][x].blocked:
                    break
    return visible