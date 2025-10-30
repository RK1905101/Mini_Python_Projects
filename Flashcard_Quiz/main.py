from utils import load_flashcards, normalize

def run_quiz(flashcards):
    score = 0
    total = len(flashcards)

    print("\n🎓 Welcome to the Flashcard Quiz!\n")

    for i, card in enumerate(flashcards, 1):
        print(f"Q{i}: {card['question']}")
        user_answer = input("Your answer: ")

        if normalize(user_answer) == normalize(card['answer']):
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {card['answer']}\n")

    print(f"🏁 Quiz Complete! You scored {score}/{total}.\n")

if __name__ == "__main__":
    flashcards = load_flashcards("flashcards.json")
    if flashcards:
        run_quiz(flashcards)