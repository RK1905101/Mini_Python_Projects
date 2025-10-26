import random

def guess_the_number():
    """
    Runs the Guess the Number game.
    The computer picks a number between 1 and 100, and the player
    has 10 attempts to guess it.
    """
    
    # --- Configuration ---
    LOWER_BOUND = 1
    UPPER_BOUND = 100
    MAX_ATTEMPTS = 10
    # ---------------------

    # Generate the secret number
    secret_number = random.randint(LOWER_BOUND, UPPER_BOUND)
    
    attempts = 0
    guessed_correctly = False

    # --- Welcome Message ---
    print("====================================")
    print("   Welcome to Guess the Number!   ")
    print("====================================")
    print(f"I'm thinking of a number between {LOWER_BOUND} and {UPPER_BOUND}.")
    print(f"You have {MAX_ATTEMPTS} attempts to guess it.")
    print("------------------------------------")

    # --- Game Loop ---
    while attempts < MAX_ATTEMPTS:
        # Display remaining attempts
        remaining_attempts = MAX_ATTEMPTS - attempts
        print(f"Attempt {attempts + 1}/{MAX_ATTEMPTS} (You have {remaining_attempts} attempts left)")

        # Get user input
        try:
            guess_str = input("Enter your guess: ")
            guess = int(guess_str)
        except ValueError:
            print("Oops! That's not a valid number. Please enter an integer.")
            print("------------------------------------")
            continue # Skip this loop iteration, doesn't count as an attempt

        # --- Check the Guess ---
        attempts += 1

        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            guessed_correctly = True
            break # Exit the loop on a correct guess
            
        print("------------------------------------")

    # --- Game Over ---
    print("====================================")
    if guessed_correctly:
        print(f"🎉 Congratulations! You guessed the number in {attempts} attempts!")
    else:
        print("😥 Game Over! You ran out of attempts.")
        print(f"The secret number was: {secret_number}")
    print("====================================")

# Run the game
if __name__ == "__main__":
    guess_the_number()
