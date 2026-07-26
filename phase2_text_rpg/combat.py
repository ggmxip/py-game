import random
from entity import Enemy
from item import get_item


def create_enemy(eid):
    t = ENEMY_TEMPLATES[eid]
    return Enemy(eid, t["hp"], t["attack"], t["defense"], t["xp"], t["gold"])


def combat_loop(player, enemy):
    print(f"\nA {enemy.name} appears!")
    while enemy.is_alive() and player.is_alive():
        print(f"\n{player.name}: {player.hp}/{player.max_hp} HP")
        print(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("1. Attack  2. Use Potion  3. Flee")
        choice = input("> ")

        if choice == "1":
            dmg = player.attack + random.randint(-2, 2)
            actual = enemy.take_damage(dmg)
            print(f"You hit the {enemy.name} for {actual} damage!")
            if enemy.is_alive():
                edmg = enemy.attack + random.randint(-2, 2)
                actual_p = player.take_damage(edmg)
                print(f"The {enemy.name} hits you for {actual_p} damage!")
        elif choice == "2":
            potions = [i for i in player.inventory if "Potion" in i]
            if not potions:
                print("No potions!")
                continue
            print(f"Potions: {', '.join(potions)}")
            pchoice = input("Use which?: ")
            item = get_item(pchoice)
            if item and hasattr(item, "heal_amount"):
                player.heal(item.heal_amount)
                player.inventory.remove(pchoice)
                print(f"Healed for {item.heal_amount} HP!")
            else:
                print("Not a potion!")
        elif choice == "3":
            if random.random() < 0.5:
                print("You fled successfully!")
                return False
            else:
                print("Failed to flee!")
                edmg = enemy.attack + random.randint(-2, 2)
                actual_p = player.take_damage(edmg)
                print(f"The {enemy.name} hits you for {actual_p} damage!")

    if not enemy.is_alive():
        print(f"\nYou defeated the {enemy.name}!")
        player.gold += enemy.gold_reward
        print(f"Gained {enemy.xp_reward} XP and {enemy.gold_reward} gold!")
        return True
    return False