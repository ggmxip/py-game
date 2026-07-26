import random
from entity import Player
from room import get_room, WORLD, ENEMY_TEMPLATES
from combat import combat_loop
from item import get_item, Weapon
import game_save


def room_enemies(enemy_list):
    enemies = []
    for e in enemy_list:
        template = ENEMY_TEMPLATES.get(e)
        if template:
            enemies.append(e)
        elif isinstance(enemy_list, dict):
            for group in enemy_list.values():
                for eid in group:
                    if eid in ENEMY_TEMPLATES:
                        enemies.append(eid)
    return enemies


def show_help():
    print("\nCommands: look, move <dir>, inventory, use <item>, save, quit, help")


def do_look(room):
    print(f"\n--- {room.name} ---")
    print(room.description)
    if room.exits:
        print(f"Exits: {', '.join(room.exits.keys())}")
    if room.items:
        print(f"You see: {', '.join(room.items)}")
    enemies = room_enemies(room.enemies)
    if enemies:
        print(f"Enemies here: {', '.join(enemies)}")


def do_move(player, direction, current_room):
    if direction not in current_room.exits:
        print("Can't go that way!")
        return current_room
    new_room_id = current_room.exits[direction]
    new_room = get_room(new_room_id)
    if new_room is None:
        print("That path is blocked!")
        return current_room
    print(f"You move {direction}.\n")
    do_look(new_room)
    return new_room_id


def do_inventory(player):
    print(f"\nGold: {player.gold}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print(f"Attack: {player.attack}  Defense: {player.defense}")
    if player.inventory:
        print(f"Items: {', '.join(player.inventory)}")
    else:
        print("Inventory is empty.")


def do_use(player, item_name, current_room):
    match = [i for i in player.inventory if item_name.lower() in i.lower()]
    if not match:
        print(f"You don't have {item_name}!")
        return False
    item_id = match[0]
    item = get_item(item_id)
    if item is None:
        print("Item not found!")
        return False
    if hasattr(item, "heal_amount"):
        player.heal(item.heal_amount)
        player.inventory.remove(item_id)
        print(f"You used {item.name}. Healed {item.heal_amount} HP!")
        return True
    elif isinstance(item, Weapon):
        old_attack = player.attack
        player.attack = 5 + item.attack_bonus
        print(f"Equipped {item.name}! Attack: {old_attack} -> {player.attack}")
        return True
    else:
        print(f"You can't use {item.name}!")
        return False


def new_game(name):
    return Player(name)


def main():
    print("=== TEXT RPG ===")

    if game_save.has_save():
        choice = input("Continue saved game? (y/n): ")
        if choice.lower() == "y":
            data = game_save.load_game()
            if data:
                player = new_game(data["name"])
                player.hp = data["hp"]
                player.attack = data["attack"]
                player.defense = data["defense"]
                player.gold = data["gold"]
                player.inventory = data["inventory"]
                current_room = data["room"]
                print("Game loaded!")
                do_look(get_room(current_room))
            else:
                print("Save corrupted. Starting new game.")
                player = new_game(input("Enter your name: "))
                current_room = "town"
                do_look(get_room(current_room))
        else:
            player = new_game(input("Enter your name: "))
            current_room = "town"
            do_look(get_room(current_room))
    else:
        player = new_game(input("Enter your name: "))
        current_room = "town"
        do_look(get_room(current_room))

    while player.is_alive():
        room = get_room(current_room)
        if room is None:
            print("You are lost in the void!")
            break

        enemies = room_enemies(room.enemies)
        if enemies:
            eid = random.choice(enemies)
            from combat import create_enemy
            enemy = create_enemy(eid)
            victory = combat_loop(player, enemy)
            if victory:
                room.enemies = [e for e in enemies if e != eid] if isinstance(room.enemies, list) else []
            else:
                if not player.is_alive():
                    print("You have died!")
                    break
                continue

        cmd = input("\n> ").strip().lower()
        if not cmd:
            continue
        parts = cmd.split(maxsplit=1)

        if cmd == "quit":
            s = input("Save before quitting? (y/n): ")
            if s.lower() == "y":
                game_save.save_game(player, current_room)
            print("Goodbye!")
            break
        elif cmd == "help":
            show_help()
        elif cmd == "look":
            do_look(get_room(current_room))
        elif cmd == "inventory" or cmd == "inv":
            do_inventory(player)
        elif cmd == "save":
            game_save.save_game(player, current_room)
        elif parts[0] == "move" and len(parts) > 1:
            current_room = do_move(player, parts[1], get_room(current_room))
        elif parts[0] == "use" and len(parts) > 1:
            do_use(player, parts[1], get_room(current_room))
        else:
            print(f"Unknown command: {cmd}. Type 'help' for commands.")


if __name__ == "__main__":
    main()