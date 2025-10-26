# 🧙‍♂️ Word Ladder CLI Game

A command-line interface (CLI) Word Ladder game in Python. Challenge your vocabulary and logic skills by transforming words one letter at a time to reach a target word. Play in Classic Mode (fewest moves) or Timed Mode (fastest time).

---

### 🌍 Gamplay

1. Choose a game mode: Classic or Timed.
2. Select a difficulty:
    - Easy → 4-letter words
    - Medium → 5-letter words
    - Hard → 6-letter words
3. The game generates a start word and a target word of the chosen length.
4. Transform the start word into the target word by changing exactly one letter at a time, forming a valid English word at each step.
5. Keep track of your moves (Classic) or your time (Timed) until you reach the target word.

---

### 🕹️ Game Modes

1. Classic Mode
    - **Goal**: Reach the target word in the fewest moves possible.
    - Moves are counted, and repeating words is not allowed.
2. Timed Mode
    - **Goal**: Reach the target word in the shortest time possible.
    - Moves are tracked but only the elapsed time counts for scoring.
---

### 🎒 Rules
1. Only one letter can be changed per move.
2. Each intermediate word must be a valid English word.
3. Repeated words are not allowed.
4. Word length must match the chosen difficulty.
5. The game ends when the current word matches the target word.

---
## ⚙ Setup
- Follow the steps to run the game

```bash
pip install colorama
python game.py 
```