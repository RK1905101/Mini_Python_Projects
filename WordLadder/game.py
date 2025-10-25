import random
import requests
import json
import os
from colorama import Fore, Style, init
from textwrap import dedent
import time
from collections import deque
import string

init(autoreset=True)

# Load all words into memory, grouped by length
def load_word_list(filename="wordList.txt"):
    words_by_length = {4: set(), 5: set(), 6: set()}
    
    with open(filename, "r") as f:
        for line in f:
            word = line.strip().lower()
            if len(word) in words_by_length:
                words_by_length[len(word)].add(word)
    
    return words_by_length
words_by_length=load_word_list()


# Fetch random word from the list
def get_random_word(word_length):
    return random.choice(list(words_by_length[word_length]))

# Check if the word is valid
def is_valid_word(word: str) -> bool:
    """Check if a word exists using dictionaryapi.dev"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    response = requests.get(url)
    return response.status_code == 200


# Check if the ladder exists between the words
def get_neighbors(word, valid_words):
    """All one-letter transformations within the valid word set."""
    neighbors = []
    for i in range(len(word)):
        for c in string.ascii_lowercase:
            if c != word[i]:
                candidate = word[:i] + c + word[i+1:]
                if candidate in valid_words:
                    neighbors.append(candidate)
    return neighbors

def has_valid_ladder(start, target, valid_words, max_depth=10):
    """Shallow BFS to ensure ladder exists."""
    visited = set([start])
    queue = deque([(start, 0)])

    while queue:
        current, depth = queue.popleft()
        if depth > max_depth:
            return False

        for neighbor in get_neighbors(current, valid_words):
            if neighbor == target:
                return True
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return False

def get_valid_word_pair(word_length, max_attempts=20):
    attempts = 0
    while attempts < max_attempts:
        start = get_random_word(word_length)
        target = get_random_word(word_length)
        if start == target:
            continue
        
        if has_valid_ladder(start, target, words_by_length[word_length]):
            return start, target
        attempts += 1

    # Fallback if no valid pair found in attempts
    return start, target

def print_title():
    title = r"""
 __        __            _     _              _     _           
 \ \      / /__  _ __ __| |   | |    __ _  __| | __| | ___ _ __ 
  \ \ /\ / / _ \| '__/ _` |   | |   / _` |/ _` |/ _` |/ _ \ '__|
   \ V  V / (_) | | | (_| |   | |__| (_| | (_| | (_| |  __/ |   
    \_/\_/ \___/|_|  \__,_|   |_____\__,_|\__,_|\__,_|\___|_|                                                           
"""
    print(Fore.CYAN + title + Style.RESET_ALL)

def print_help():
    print(Fore.YELLOW + dedent("""
    Commands:
      - Type a new word differing by ONE letter
      - 'h'     Show this help message
      - 'q'     Exit the game
      - 'r'     Restart the current mode
    """) + Style.RESET_ALL)
    
# High Scores
def save_high_score(mode, word_length, moves, start_word, target_word):
    filename = "highscores.json"
    data = []

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)

    data.append({
        "mode": mode,
        "length": word_length,
        "moves": moves,
        "start": start_word,
        "target": target_word
    })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(Fore.YELLOW + f"\nHigh score saved to {filename}" + Style.RESET_ALL)


# Main Game Logic
def play_game(mode):
    print(Fore.MAGENTA + f"Welcome to the {mode.upper()} mode of Word Ladder!" + Style.RESET_ALL)

    difficulties = {1: 4, 2: 5, 3: 6}
    print(Fore.GREEN + "\nChoose difficulty level:")
    print("1. Easy (4-letter words)\n2. Medium (5-letter words)\n3. Hard (6-letter words)")

    while True:
        try:
            choice = int(input(Fore.CYAN + "Enter difficulty (1-3): " + Style.RESET_ALL))
            if choice in difficulties:
                word_length = difficulties[choice]
                break
            else:
                print(Fore.RED + "Invalid choice. Please choose 1, 2, or 3.")
        except ValueError:
            print(Fore.RED + "Please enter a number (1-3).")

    print(Fore.MAGENTA + f"\nGenerating random {word_length}-letter words..." + Style.RESET_ALL)
    start_word, target_word = get_valid_word_pair(word_length)

    print(Fore.GREEN + f"Start word: {start_word} → Target word: {target_word}")
    print_help()

    current_word = start_word
    used_words = {start_word}
    moves = 0
    start_time = time.time()

    while current_word != target_word:
        guess = input(Fore.CYAN + f"\nCurrent word: {current_word}\nEnter next word: " + Style.RESET_ALL).lower()

        if guess == 'q':
            print(Fore.YELLOW + "You quit the game!" + Style.RESET_ALL)
            return
        if guess == 'h':
            print_help()
            continue
        if guess == 'r':
            print(Fore.YELLOW + "Restarting game...\n" + Style.RESET_ALL)
            return play_game(mode)

        if len(guess) != word_length:
            print(Fore.RED + f"Word must be {word_length} letters long.")
            continue
        if guess in used_words:
            print(Fore.RED + "You already used this word.")
            continue

        # Check one-letter difference
        diff = sum(a != b for a, b in zip(current_word, guess))
        if diff != 1:
            print(Fore.RED + "You can only change ONE letter per move.")
            continue

        # Must be in word list
        if not is_valid_word(guess):
            print(Fore.RED + "That’s not a valid English word.")
            continue

        # Valid move
        used_words.add(guess)
        current_word = guess
        moves += 1

        if mode == "timed":
            elapsed = time.time() - start_time
            print(Fore.GREEN + f"Good move! ({moves} steps so far, {elapsed:.2f}s elapsed)" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Good move! ({moves} moves so far)" + Style.RESET_ALL)

    # End of game
    elapsed = time.time() - start_time
    if mode == "timed":
        print(Fore.CYAN + f"\n🎉 You reached '{target_word}' in {elapsed:.2f} seconds! 🎉" + Style.RESET_ALL)
        save_high_score(mode, word_length, elapsed, start_word, target_word)
    else:
        print(Fore.CYAN + f"\n🎉 You reached '{target_word}' in {moves} moves! 🎉" + Style.RESET_ALL)
        save_high_score(mode, word_length, moves, start_word, target_word)


# Entry point of the game
def main():
    print_title()
    print(Fore.MAGENTA + "Welcome to Word Ladder CLI!\n" + Style.RESET_ALL)
    print(Fore.GREEN + "Choose Game Mode:")
    print("1. Classic Mode (Fewest moves wins)")
    print("2. Timed Mode (Fastest time wins)")

    while True:
        try:
            choice = int(input(Fore.CYAN + "Enter choice (1-2): " + Style.RESET_ALL))
            if choice == 1:
                play_game("classic")
                break
            elif choice == 2:
                play_game("timed")
                break
            else:
                print(Fore.RED + "Invalid choice. Enter 1 or 2.")
        except ValueError:
            print(Fore.RED + "Please enter a number (1 or 2).")

if __name__ == "__main__":
    main()
