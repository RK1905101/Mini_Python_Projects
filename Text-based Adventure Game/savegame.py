import json
import os
from typing import Dict
from player import Player
from utils import ctext

SAVEFILE = 'savegames.json'


# Load all player saves from the savegames.json file
def load_all_saves() -> Dict[str, dict]:
    if not os.path.exists(SAVEFILE):
        return {}
    try:
        with open(SAVEFILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(ctext("⚠️ Corrupted save file. Starting fresh.", "RED"))
        return {}


# Write all saves back to the file
def save_all_saves(data: Dict[str, dict]):
    with open(SAVEFILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


# Save a specific player's progress
def save(player: Player):
    all_saves = load_all_saves()
    all_saves[player.name] = player.to_dict()
    save_all_saves(all_saves)
    print(ctext(f"💾 Game saved for {player.name}.", "GREEN"))


# Load the save for a specific player name
def load(name: str) -> Player:
    all_saves = load_all_saves()
    if name in all_saves:
        print(ctext(f"📂 Loaded save for {name}.", "GREEN"))
        return Player.from_dict(all_saves[name])
    print(ctext(f"⚠️ No save found for player '{name}'. Starting a new game.", "YELLOW"))
    return None


# Delete a specific player's save
def delete_save(name: str):
    all_saves = load_all_saves()
    if name in all_saves:
        confirm = input(ctext(f"Delete save for {name}? (Y/N): ", "YELLOW")).strip().upper()
        if confirm == 'Y':
            del all_saves[name]
            save_all_saves(all_saves)
            print(ctext(f"🗑️ Save deleted for {name}.", "GREEN"))
        else:
            print(ctext("Deletion cancelled.", "CYAN"))
    else:
        print(ctext(f"No save found for player '{name}'.", "YELLOW"))
