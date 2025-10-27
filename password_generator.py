import random
import string

def generate_strong_password(length=12):
    """
    Generates a strong, random password of a specified length.
    Includes a mix of uppercase, lowercase, digits, and symbols.
    """
    if length < 4:
        print("Password length must be at least 4 to ensure a strong mix of characters.")
        length = 4

    # Define the character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    all_chars = lower + upper + digits + symbols

    password = []

    # Ensure the password contains at least one of each character type for strength
    password.append(random.choice(lower))
    password.append(random.choice(upper))
    password.append(random.choice(digits))
    password.append(random.choice(symbols))

    # Fill the remaining length with random choices from all characters
    for _ in range(length - 4):
        password.append(random.choice(all_chars))

    # Shuffle the list to ensure randomness and not have the required characters at the start
    random.shuffle(password)

    # Convert the list back to a string
    return "".join(password)

if __name__ == "__main__":
    try:
        # Get desired length from the user
        input_length = input("Enter the desired password length (default is 12): ")

        # Use 12 as default if user just presses enter, otherwise convert to int
        if input_length.strip() == "":
            length = 12
        else:
            length = int(input_length)

        # Generate and print the password
        password = generate_strong_password(length)
        print(f"\nGenerated Strong Password ({len(password)} characters):")
        print(password)

    except ValueError:
        print("\nInvalid input. Please enter a whole number for the length.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")