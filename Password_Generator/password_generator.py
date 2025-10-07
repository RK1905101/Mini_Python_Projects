import random
import string

def generate_password(length=12, use_upper=True, use_lower=True, 
                     use_digits=True, use_special=True):
    """Generate a random password with specified criteria."""
    
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        return "Error: Please select at least one character type!"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    print("=" * 50)
    print("       PASSWORD GENERATOR")
    print("=" * 50)
    
    try:
        length = int(input("\nEnter password length (default 12): ") or 12)
        use_upper = input("Include uppercase letters? (y/n, default y): ").lower() != 'n'
        use_lower = input("Include lowercase letters? (y/n, default y): ").lower() != 'n'
        use_digits = input("Include digits? (y/n, default y): ").lower() != 'n'
        use_special = input("Include special characters? (y/n, default y): ").lower() != 'n'
        
        password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        
        print("\n" + "=" * 50)
        print(f"Generated Password: {password}")
        print("=" * 50)
        
    except ValueError:
        print("Invalid input! Please enter a valid number for length.")

if __name__ == "__main__":
    main()