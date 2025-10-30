import random

# ASCII art for dice faces
DICE_ART = {
    1: (
        "+-------+",
        "|       |",
        "|   •   |",
        "|       |",
        "+-------+",
    ),
    2: (
        "+-------+",
        "| •     |",
        "|       |",
        "|     • |",
        "+-------+",
    ),
    3: (
        "+-------+",
        "| •     |",
        "|   •   |",
        "|     • |",
        "+-------+",
    ),
    4: (
        "+-------+",
        "| •   • |",
        "|       |",
        "| •   • |",
        "+-------+",
    ),
    5: (
        "+-------+",
        "| •   • |",
        "|   •   |",
        "| •   • |",
        "+-------+",
    ),
    6: (
        "+-------+",
        "| •   • |",
        "| •   • |",
        "| •   • |",
        "+-------+",
    ),
}

def roll_dice(num_dice: int):
    """Roll the dice and return results."""
    rolls = [random.randint(1, 6) for _ in range(num_dice)]
    return rolls

def display_dice(rolls):
    """Display ASCII art for dice results."""
    dice_faces = [DICE_ART[roll] for roll in rolls]
    for i in range(5):  # each face has 5 lines
        print("   ".join(dice[i] for dice in dice_faces))

def main():
    print("🎲 Welcome to the Dice Rolling Simulator! 🎲")
    while True:
        try:
            num_dice = int(input("\nHow many dice do you want to roll? (1-2): "))
            if num_dice not in (1, 2):
                print("❌ Please enter 1 or 2.")
                continue
        except ValueError:
            print("❌ Invalid input. Enter a number.")
            continue

        rolls = roll_dice(num_dice)
        print("\nYour roll:")
        display_dice(rolls)

        again = input("\nRoll again? (y/n): ").lower()
        if again != "y":
            print("👋 Thanks for playing!")
            break

if __name__ == "__main__":
    main()
