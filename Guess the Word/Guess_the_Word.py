import random
import sys

# --- Configuration ---
WORDS = [
    "python", "programming", "developer", "computer", "algorithm",
    "challenge", "keyboard", "variable", "function", "module",
    "terminal", "instance", "software", "hardware", "internet"
]
MAX_ATTEMPTS = 6

def choose_word(word_list):
    """Randomly selects a word from the provided list."""
    return random.choice(word_list).upper()

def display_game_state(word, guessed_letters):
    """
    Creates and returns the hidden word string with guessed letters filled in.
    e.g., if word is 'PYTHON' and guessed_letters is {'P', 'O'}, returns 'P Y T H O N'
    """
    displayed_word = []
    for letter in word:
        if letter in guessed_letters:
            displayed_word.append(letter)
        else:
            displayed_word.append('_')
    return ' '.join(displayed_word)

def play_game():
    print("--- Welcome to GUESS THE WORD! ---")
    print(f"You have {MAX_ATTEMPTS} incorrect guesses before the game ends.")
    print("Let's begin!")

    secret_word = choose_word(WORDS)
    guessed_letters = set()
    incorrect_guesses = 0
    
    all_tried_letters = set() 

    while incorrect_guesses < MAX_ATTEMPTS:
        current_display = display_game_state(secret_word, guessed_letters)
        
        print("\n" + "="*40)
        print(f"Word: {current_display}")
        print(f"Attempts Remaining: {MAX_ATTEMPTS - incorrect_guesses}")
        print(f"Letters Guessed: {sorted(list(all_tried_letters))}")
        print("="*40)

        #  Check for Win condition
        if '_' not in current_display:
            print(f"\n🥳 Congratulations! You guessed the word: {secret_word} 🥳")
            return

        # Get user input
        while True:
            try:
                guess = input("Guess a letter: ").strip().upper()
                
                if not guess.isalpha() or len(guess) != 1:
                    print("🚫 Invalid input. Please enter a single letter (A-Z).")
                    continue
                
                if guess in all_tried_letters:
                    print(f"💡 You already tried the letter '{guess}'. Try a new one!")
                    continue
                
                break
            except EOFError:
                print("\nGame session ended. Goodbye!")
                return
        
        all_tried_letters.add(guess)

        #  Process the guess
        if guess in secret_word:
            print(f"✅ Great guess! The letter '{guess}' is in the word.")
            guessed_letters.add(guess)
        else:
            print(f"❌ Oops! The letter '{guess}' is NOT in the word.")
            incorrect_guesses += 1
    
    print("\n" + "#"*40)
    print("GAME OVER! You ran out of attempts.")
    print(f"The secret word was: {secret_word}")
    print("#"*40)

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Thanks for playing!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
