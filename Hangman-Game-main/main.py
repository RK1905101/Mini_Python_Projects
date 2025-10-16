import random
import os
from words import word_categories, get_random_word
from hangman_art import stages, logo, win_art, lose_art

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_game_state(word_progress, incorrect_guesses, lives, guessed_letters):
    """Display current game state"""
    clear_screen()
    print(logo)
    print(f"\n{stages[lives]}")
    print(f"\nWord: {' '.join(word_progress)}")
    print(f"\nLives remaining: {'❤️ ' * lives}")
    print(f"Incorrect guesses: {', '.join(sorted(incorrect_guesses)) if incorrect_guesses else 'None'}")
    print(f"All guessed letters: {', '.join(sorted(guessed_letters))}")

def get_difficulty():
    """Get difficulty level from player"""
    print("\n🎯 Select Difficulty Level:")
    print("1. Easy (6-8 letter words, 8 lives)")
    print("2. Medium (5-7 letter words, 6 lives)")
    print("3. Hard (4-6 letter words, 5 lives)")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("❌ Invalid choice! Please enter 1, 2, or 3.")

def get_category():
    """Get word category from player"""
    print("\n📚 Select Word Category:")
    categories = list(word_categories.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    while True:
        choice = input(f"\nEnter your choice (1-{len(categories)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print(f"❌ Invalid choice! Please enter a number between 1 and {len(categories)}.")

def get_hint(word, word_progress, hints_remaining):
    """Provide a hint by revealing a random unrevealed letter"""
    if hints_remaining <= 0:
        return None, 0
    
    unrevealed_indices = [i for i, letter in enumerate(word_progress) if letter == '_']
    if unrevealed_indices:
        hint_index = random.choice(unrevealed_indices)
        return word[hint_index], hints_remaining - 1
    return None, hints_remaining

def play_game():
    """Main game logic"""
    clear_screen()
    print(logo)
    print("\n🎮 Welcome to Hangman! 🎮")
    print("=" * 50)
    
    # Setup game
    difficulty = get_difficulty()
    category = get_category()
    
    # Set lives based on difficulty
    lives_map = {'1': 8, '2': 6, '3': 5}
    max_lives = lives_map[difficulty]
    lives = max_lives
    
    # Get word
    word = get_random_word(category, difficulty)
    word_progress = ['_'] * len(word)
    guessed_letters = set()
    incorrect_guesses = set()
    
    # Hint system
    max_hints = 2 if difficulty == '1' else 1 if difficulty == '2' else 0
    hints_remaining = max_hints
    
    # Score tracking
    score = 0
    
    game_over = False
    won = False
    
    while not game_over:
        display_game_state(word_progress, incorrect_guesses, lives, guessed_letters)
        
        # Show hints available
        if hints_remaining > 0:
            print(f"\n💡 Hints remaining: {hints_remaining}")
        
        # Get player input
        print("\n" + "=" * 50)
        guess = input("Guess a letter (or type 'hint' for a hint): ").lower().strip()
        
        # Handle hint request
        if guess == 'hint':
            if hints_remaining > 0:
                hint_letter, hints_remaining = get_hint(word, word_progress, hints_remaining)
                if hint_letter:
                    print(f"\n💡 Hint: The word contains the letter '{hint_letter.upper()}'")
                    input("Press Enter to continue...")
                else:
                    print("\n❌ No more letters to reveal!")
                    input("Press Enter to continue...")
            else:
                print("\n❌ No hints remaining!")
                input("Press Enter to continue...")
            continue
        
        # Validate input
        if len(guess) != 1:
            print("\n❌ Please enter only ONE letter!")
            input("Press Enter to continue...")
            continue
        
        if not guess.isalpha():
            print("\n❌ Please enter a valid letter (A-Z)!")
            input("Press Enter to continue...")
            continue
        
        if guess in guessed_letters:
            print(f"\n⚠️ You already guessed '{guess.upper()}'! Try another letter.")
            input("Press Enter to continue...")
            continue
        
        # Process guess
        guessed_letters.add(guess)
        
        if guess in word:
            # Correct guess
            for i, letter in enumerate(word):
                if letter == guess:
                    word_progress[i] = guess
            
            print(f"\n✅ Correct! '{guess.upper()}' is in the word!")
            score += 10
            
            # Check if won
            if '_' not in word_progress:
                game_over = True
                won = True
        else:
            # Incorrect guess
            incorrect_guesses.add(guess)
            lives -= 1
            print(f"\n❌ Wrong! '{guess.upper()}' is not in the word. You lose a life!")
            
            # Check if lost
            if lives == 0:
                game_over = True
                won = False
        
        if not game_over:
            input("Press Enter to continue...")
    
    # Game over screen
    clear_screen()
    print(logo)
    
    if won:
        print(win_art)
        print(f"\n🎉 CONGRATULATIONS! You won! 🎉")
        print(f"\nThe word was: {word.upper()}")
        
        # Calculate final score
        bonus = lives * 20
        hint_penalty = (max_hints - hints_remaining) * 5
        final_score = score + bonus - hint_penalty
        
        print(f"\n📊 Your Score:")
        print(f"   Base score: {score}")
        print(f"   Lives bonus: +{bonus}")
        if hint_penalty > 0:
            print(f"   Hint penalty: -{hint_penalty}")
        print(f"   Final Score: {final_score} 🌟")
    else:
        print(lose_art)
        print(f"\n💀 GAME OVER! You lost! 💀")
        print(f"\nThe word was: {word.upper()}")
        print(f"You were so close! Better luck next time! 💪")
    
    return won, final_score if won else 0

def main():
    """Main game loop"""
    clear_screen()
    print(logo)
    print("\n" + "=" * 50)
    print("🎮 HANGMAN GAME 🎮".center(50))
    print("=" * 50)
    input("\nPress Enter to start...")
    
    total_games = 0
    total_wins = 0
    total_score = 0
    win_streak = 0
    best_streak = 0
    
    play_again = True
    
    while play_again:
        won, score = play_game()
        
        total_games += 1
        total_score += score
        
        if won:
            total_wins += 1
            win_streak += 1
            if win_streak > best_streak:
                best_streak = win_streak
        else:
            win_streak = 0
        
        # Show statistics
        print("\n" + "=" * 50)
        print("📈 YOUR STATISTICS:")
        print(f"   Games played: {total_games}")
        print(f"   Games won: {total_wins}")
        print(f"   Win rate: {(total_wins/total_games)*100:.1f}%")
        print(f"   Total score: {total_score}")
        print(f"   Current streak: {win_streak} 🔥" if win_streak > 0 else f"   Current streak: {win_streak}")
        print(f"   Best streak: {best_streak}")
        print("=" * 50)
        
        # Ask to play again
        while True:
            choice = input("\nDo you want to play again? (yes/no): ").lower().strip()
            if choice in ['yes', 'y']:
                play_again = True
                break
            elif choice in ['no', 'n']:
                play_again = False
                break
            else:
                print("❌ Please enter 'yes' or 'no'.")
    
    # Goodbye message
    clear_screen()
    print(logo)
    print("\n" + "=" * 50)
    print("👋 Thanks for playing Hangman! 👋".center(50))
    print("=" * 50)
    print(f"\n🏆 Final Statistics:")
    print(f"   Games played: {total_games}")
    print(f"   Games won: {total_wins}")
    print(f"   Win rate: {(total_wins/total_games)*100:.1f}%")
    print(f"   Total score: {total_score}")
    print(f"   Best streak: {best_streak}")
    print("\n" + "=" * 50)
    print("See you next time! 🎮".center(50))
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
