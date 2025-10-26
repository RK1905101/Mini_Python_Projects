# 🧙‍♂️ Text-Based Adventure Game

An interactive, story-driven Python adventure where your choices shape the outcome. Battle enemies, collect items, face random challenges, and unlock multiple endings — all through a dynamic text interface.

---

### 🌍 Overview

You are an explorer trapped in an ancient dungeon. Your goal is to escape safely — but how you survive depends on your decisions, luck, and courage.

The game features branching storylines, an inventory system, player stats, and a modular code structure for easy expansion.

---

### 🕹️ Gameplay Flow

1. Introduction – The story and world are introduced.
2. Decision Points – Players make choices that affect the storyline.
3. Combat & Random Events – Encounter enemies and roll dice (or now, choose your own roll).
4. Inventory & Stats – Items and attributes affect outcomes.
5. Endings – Reach one of several good, bad, or secret endings based on your journey.
---

### 🎒 Items You Can Find
Throughout your journey, you may collect or use:
| Item               | Purpose                                                               |
| ------------------ | --------------------------------------------------------------------- |
| 🗡️ **Dagger**     | Boosts attack power during combat.                                    |
| 🗺️ **Map**        | Reveals hidden paths and symbols (used for the Warden’s rune puzzle). |
| 🧪 **Potion**      | Can be used to weaken the final boss (Warden debuff).                 |
| 🔑 **Rusty Key**         | Opens locked areas or gates.                                          |
| 💎 **Gem**         | Valuable artifact, may influence certain endings.                     |
| 📜 **Rune Scroll** | Grants knowledge or magical insight in specific encounters.           |
---

### ⚔️ Combat Rules

1. You and the enemy each roll for attack.
    - You choose your roll number.
    - The enemy’s roll is random.
2. Higher total of the (roll + strength) wins the round.
3. Loser takes damage based on the attacker’s strength.
4. Enemy and player HP are displayed after each roll.
5. Special bosses (like the Warden) can regenerate or be weakened using special items
---
### 💾 Save and Load Game System
The game supports a persistent save system that allows each player to save, resume, or delete their progress, seperately. So that a player can resume their saved game anytime again in future.

---
## ⚙ Setup
- Follow the steps to run the game

```bash
pip install colorama
python game.py 
```