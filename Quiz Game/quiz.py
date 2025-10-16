import random
import json
import time

# Load questions from a JSON file
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)["questions"]


# Select a random set of questions up to the specified number
def get_random_questions(questions, num_questions):
    return random.sample(questions, min(num_questions, len(questions)))


# Ask a single question, handle input, and check if the answer is correct
def ask_question(question):
    print("\n" + question["question"])
    options = question["options"][:]
    random.shuffle(options)       # Shuffle options

    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    while True:
        try:
            choice = int(input("👉 Select the correct number: "))
            if 1 <= choice <= len(options):
                break
            else:
                print("❌ Please choose a valid option number.")
                
        except ValueError:
            print("❌ Please enter a number.")

    # Check if the selected option is correct
    selected_option = options[choice - 1]
    if selected_option == question["answer"]:
        print("✅ Correct!\n")
        return True
    else:
        print(f"❌ Incorrect! The correct answer was: {question['answer']}\n")
        return False


def play_quiz():
    questions = load_questions()
    total_questions = int(input("\nHow many questions would you like to attempt? "))
    random_questions = get_random_questions(questions, total_questions)

    correct = 0
    start_time = time.time()  # Start the timer

    # Ask each question in sequence
    for i, question in enumerate(random_questions, 1):
        print(f"\nQuestion {i} of {total_questions}:")
        if ask_question(question):
            correct += 1
        print("-" * 30)

    duration = time.time() - start_time  # Calculate total time taken

    print("\n📊 Quiz Summary")
    print(f"✅ Correct Answers: {correct}")
    print(f"❌ Wrong Answers: {total_questions - correct}")
    print(f"🎯 Score: {round((correct / total_questions) * 100, 2)}%")
    print(f"⏱️  Time Taken: {round(duration, 2)} seconds")


if __name__ == "__main__":

    print("🎉 --- Welcome to the Quiz Game ---🎉")
    while True:
        play_quiz()
        replay = input("\nDo you want to play again? (y/n): ").strip().lower()

        if replay != 'y':
            print("👋 Thanks for playing!")
            break
