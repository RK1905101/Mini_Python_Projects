import sys
import json
import os
from colorama import init
init(autoreset=True)

from player import Player
from manager import StoryManager
from combat import CombatSystem
from savegame import load, save, delete_save
from utils import ctext, ASCII_TITLE


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_choice(prompt: str, valid: set):
    choice = input(ctext(prompt, 'YELLOW') + ' ').strip().upper()
    while choice not in valid:
        print(ctext('Invalid choice. Try again.', 'RED'))
        choice = input(ctext(prompt, 'YELLOW') + ' ').strip().upper()
    return choice


def main():
    clear_screen()
    print(ctext(ASCII_TITLE, 'GREEN'))
    print(ctext('A Text-Based Adventure — Fight the Warden'))
    name = input(ctext('Enter your name (or press Enter):', 'MAGENTA') + ' ').strip() or 'Adventurer'

    # load story
    sm = StoryManager('story.json')

    # load or new
    existing = load(name)
    if existing:
        use = input(ctext(f"A save for {name} was found. Load it? (Y/N): ", 'CYAN')).strip().upper()
        if use == 'Y':
            player = existing
        else:
            player = Player(name)
    else:
        player = Player(name)

    combat = CombatSystem(player)

    while True:
        node = sm.get_node(player.node)
        if not node:
            print(ctext('Error: story node not found: ' + str(player.node), 'RED'))
            break
        print('\n' + ctext(node.get('title',''), 'CYAN'))
        print(node.get('text') + '\n')

        choices = sm.list_choices(node)
        # display choices that meet requirements
        valid_keys = set()
        for k, ch in choices.items():
            req = ch.get('requirements')
            if req and 'items' in req:
                if not player.has_items(req['items']):
                    # indicate locked choice
                    print(ctext(f"[{k}] {ch['text']} (locked - missing items)", 'YELLOW'))
                    continue
            print(ctext(f"[{k}] {ch['text']}", 'BLUE'))
            valid_keys.add(k)

        # utility commands
        print(ctext('[I] Inventory   [Save] Save   [Load] Load   [Delete] Delete Save   [Q] Quit', 'MAGENTA'))
        choice_raw = input(ctext('Choose', 'YELLOW') + ' ').strip()
        choice = choice_raw.upper()

        if not choice:
            continue
        if choice == 'Q':
            print(ctext('Goodbye!', 'GREEN'))
            break
        if choice == 'I':
            print(ctext(f"Name: {player.name} | HP: {player.health}/{player.max_health} | STR: {player.strength}", 'CYAN'))
            print(ctext('Inventory: ' + (', '.join(player.inventory) or 'Empty'), 'CYAN'))
            continue
        if choice_raw.lower() == 'save':
            save(player)
            print(ctext('Game saved.', 'GREEN'))
            continue
        if choice_raw.lower() == 'load':
            loaded = load()
            if loaded:
                player = loaded
                combat = CombatSystem(player)
                print(ctext('Save loaded.', 'GREEN'))
            else:
                print(ctext('No save found.', 'YELLOW'))
            continue
        if choice_raw.lower() == 'delete':
            delete_save(player.name)
            continue


        # choice handling
        if choice in choices:
            ch = choices[choice]
            req = ch.get('requirements')
            if req and 'items' in req and not player.has_items(req['items']):
                print(ctext('You lack required items for that choice.', 'YELLOW'))
                continue
            # apply effects
            eff = ch.get('effects')
            player.apply_effects(eff)

            # special cases for combat nodes
            target = ch.get('target')
            if target in ('combat_warden_fight','combat_warden'):
                # Armory Warden (enhanced enemy)
                won, log = combat.simple_enemy('Armory Warden', hp=12, strength=4)
                print(log)
                if won:
                    print(ctext('You defeated the Armory Warden!', 'GREEN'))
                    # maybe drop key
                    if 'rusty_key' not in player.inventory:
                        player.inventory.append('rusty_key')
                        print(ctext('You find a rusty key among the remains.', 'CYAN'))
                    player.node = 'left_door'
                else:
                    print(ctext('You were slain by the Warden...', 'RED'))
                    print(ctext('Game over.', 'RED'))
                    break
                continue

            if target in ('combat_eel_fight','combat_eel'):
                won, log = combat.simple_enemy('Cave Eel', hp=8, strength=3)
                print(log)
                if won:
                    print(ctext('You fought off the eel and surface.', 'GREEN'))
                    if 'iron_key' not in player.inventory:
                        player.inventory.append('iron_key')
                    player.node = 'right_pool'
                else:
                    print(ctext('The eel drags you under...', 'RED'))
                    break
                continue

            if target == 'final_combat' or target == 'ending_outcome':
                # Final boss
                # Determine Warden stats
                warden_hp = 20
                warden_str = 5
                if player.warden_debuff:
                    warden_hp -= 6
                won, log = combat.simple_enemy('Skeletal Warden', hp=warden_hp, strength=warden_str)
                print(log)
                if won:
                    print(ctext('You topple the Warden. The curse lifts. You escape!', 'GREEN'))
                    print(ctext('ENDING: Triumph — You escaped the dungeon.', 'GREEN'))
                else:
                    if player.health > 0:
                        print(ctext('You stagger away but the dungeon keeps its secrets. Bittersweet escape.', 'YELLOW'))
                        print(ctext('ENDING: Bittersweet — You barely escaped.', 'YELLOW'))
                    else:
                        print(ctext('You fall. The Warden claims another victim.', 'RED'))
                        print(ctext('ENDING: Tragic — You died in the depths.', 'RED'))
                break

            player.node = target
            continue

        else:
            print(ctext('That option is not available here.', 'YELLOW'))
            continue

if __name__ == '__main__':
    if '--bootstrap' in sys.argv:
        content = sys.modules[__name__].__doc__
    main()