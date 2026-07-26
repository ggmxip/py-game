import tcod
import tcod.event
from entity import Player, Enemy
from map_gen import generate_dungeon, place_entities, Tile
from fov import calculate_fov

WIDTH, HEIGHT = 60, 40
MAP_W, MAP_H = 60, 40

FLOOR_CHAR = "."
WALL_CHAR = "#"

COLOR_FLOOR = (50, 50, 50)
COLOR_WALL = (100, 100, 100)
COLOR_FLOOR_VISIBLE = (80, 80, 80)
COLOR_WALL_VISIBLE = (130, 130, 100)
COLOR_FLOOR_EXPLORED = (40, 40, 40)
COLOR_WALL_EXPLORED = (70, 70, 60)
COLOR_PLAYER = (255, 255, 0)
COLOR_ENEMY = (255, 50, 50)
COLOR_HP_BAR = (255, 0, 0)
COLOR_HP_BG = (80, 0, 0)


def render(console, player, game_map, visible, enemies):
    console.clear()
    w, h = len(game_map[0]), len(game_map)

    for y in range(h):
        for x in range(w):
            tile = game_map[y][x]
            visible_now = (x, y) in visible
            explored = tile.explored or visible_now

            if not explored:
                continue

            if tile.blocked:
                color = COLOR_WALL_VISIBLE if visible_now else COLOR_WALL_EXPLORED
                console.print(x, y, WALL_CHAR, fg=color)
            else:
                color = COLOR_FLOOR_VISIBLE if visible_now else COLOR_FLOOR_EXPLORED
                console.print(x, y, FLOOR_CHAR, fg=color)

            if visible_now and not tile.explored:
                tile.explored = True

    if (player.x, player.y) in visible:
        console.print(player.x, player.y, "@", fg=COLOR_PLAYER)

    for e in enemies:
        if (e.x, e.y) in visible and e.hp > 0:
            console.print(e.x, e.y, e.char, fg=COLOR_ENEMY)

    hp_text = f"HP: {player.hp}/{player.max_hp}"
    for i, ch in enumerate(hp_text):
        console.print(i, 0, ch, fg=(255, 255, 255))


def get_path(start, end, game_map):
    open_set = {start}
    closed = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - end[0]) + abs(start[1] - end[1])}

    while open_set:
        current = min(open_set, key=lambda p: f_score.get(p, 9999))
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        open_set.remove(current)
        closed.add(current)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if neighbor in closed:
                continue
            if not (0 <= nx < MAP_W and 0 <= ny < MAP_H):
                continue
            if game_map[ny][nx].blocked:
                continue
            g = g_score[current] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif g >= g_score.get(neighbor, 9999):
                continue
            came_from[neighbor] = current
            g_score[neighbor] = g
            f_score[neighbor] = g + abs(nx - end[0]) + abs(ny - end[1])
    return []


def main():
    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)
    console = tcod.Console(WIDTH, HEIGHT)
    context = tcod.context.new(columns=WIDTH, rows=HEIGHT, tileset=tileset)

    game_map, rooms = generate_dungeon(MAP_W, MAP_H)
    player = Player(0, 0)
    enemies = place_entities(rooms, player)
    player.fov_radius = 8

    running = True
    turn = "player"

    while running:
        visible = calculate_fov(player.x, player.y, player.fov_radius, game_map)
        render(console, player, game_map, visible, enemies)
        context.present(console)

        for event in tcod.event.wait():
            if event.type == "QUIT":
                running = False
                break

            if event.type == "KEYDOWN":
                if event.sym == tcod.event.K_ESCAPE:
                    running = False
                    break

                dx, dy = 0, 0
                if event.sym == tcod.event.K_UP or event.sym == tcod.event.K_w:
                    dy = -1
                elif event.sym == tcod.event.K_DOWN or event.sym == tcod.event.K_s:
                    dy = 1
                elif event.sym == tcod.event.K_LEFT or event.sym == tcod.event.K_a:
                    dx = -1
                elif event.sym == tcod.event.K_RIGHT or event.sym == tcod.event.K_d:
                    dx = 1
                else:
                    continue

                if dx != 0 or dy != 0:
                    new_x, new_y = player.x + dx, player.y + dy
                    blocked_by_enemy = False
                    for e in enemies:
                        if e.x == new_x and e.y == new_y and e.hp > 0:
                            dmg = e.take_damage(player.attack)
                            print(f"Hit {e.name} for {dmg} damage!")
                            if e.hp <= 0:
                                print(f"{e.name} dies!")
                            blocked_by_enemy = True
                            break
                    if not blocked_by_enemy:
                        player.move(dx, dy, game_map)
                    turn = "enemy"

        if turn == "enemy":
            for e in enemies:
                if e.hp <= 0:
                    continue
                if player.distance_to(e) <= 6:
                    path = get_path((e.x, e.y), (player.x, player.y), game_map)
                    if path and len(path) > 0:
                        nx, ny = path[0]
                        if nx == player.x and ny == player.y:
                            dmg = max(1, e.attack - player.defense)
                            player.hp -= dmg
                            print(f"{e.name} hits you for {dmg} damage!")
                            if player.hp <= 0:
                                print("You die! Game over!")
                                running = False
                        else:
                            e.x, e.y = nx, ny
            turn = "player"


if __name__ == "__main__":
    main()