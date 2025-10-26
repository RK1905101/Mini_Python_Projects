import random
from typing import Tuple

from player import Player

class CombatSystem:
    def __init__(self, player: Player):
        self.player = player

    def roll(self, sides=6) -> int:
        return random.randint(1, sides)

    def simple_enemy(self, name: str, hp: int, strength: int) -> Tuple[bool, str]:
        # Returns (player_won, summary)
        log = []
        enemy_hp = hp
        log.append(f"A {name} appears! (HP {hp}, STR {strength})")

        while enemy_hp > 0 and self.player.health > 0:
            print("\n" + "-" * 40)
            print(f"⚔️  {name}: HP {enemy_hp}, STR {strength}")
            print(f"🧍  {self.player.name}: HP {self.player.health}/{self.player.max_health}, STR {self.player.strength}")
            print("-" * 40)
            
            # --- Player manually chooses roll ---
            while True:
                try:
                    player_roll = int(input(f"Choose your roll (1-6): "))
                    if 1 <= player_roll <= 6:
                        break
                    else:
                        print("Please enter a number between 1 and 6.")
                except ValueError:
                    print("Invalid input. Enter an integer between 1 and 6.")

            # --- Enemy rolls randomly ---
            enemy_roll = self.roll() + strength

            total_player = player_roll + self.player.strength
            log.append(f"You chose {player_roll} (+{self.player.strength} STR) = {total_player} vs enemy {enemy_roll}")

            # --- Compare rolls ---
            if total_player >= enemy_roll:
                damage = max(1, self.player.strength + self.roll() - 2)
                enemy_hp -= damage
                log.append(f"You hit for {damage}! Enemy HP now {max(enemy_hp, 0)}")
            else:
                damage = max(1, strength + self.roll() - 2)
                self.player.health -= damage
                log.append(f"Enemy hits for {damage}! Your HP now {max(self.player.health, 0)}")

            # --- Warden regen mechanic ---
            if "warden" in name.lower() and not getattr(self.player, "warden_debuff", False):
                enemy_hp += 1  # regenerative curse
                log.append(f"The {name} regenerates slightly (+1 HP)! Now at {enemy_hp} HP.")

            log.append("-" * 40)

        # --- Outcome ---
        won = enemy_hp <= 0 and self.player.health > 0
        return won, "\n".join(log)

