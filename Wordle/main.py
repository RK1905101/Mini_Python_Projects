from rich.console import Console
from rich.prompt import Prompt
from words import word_list
from random import choice

MAX_GUESSES = 6

SQUARES = {"correct_place": "🟩", "correct_letter": "🟨", "incorrect_letter": "⬛"}

def correct_place(letter):
    return f"[black on green]{letter}[/]"


def correct_letter(letter):
    return f"[black on yellow]{letter}[/]"


def incorrect_letter(letter):
    return f"[black on white]{letter}[/]"


def check_guess(guess, answer):
    guessed = []
    wordle_pattern = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            guessed += correct_place(letter)
            wordle_pattern.append(SQUARES["correct_place"])
        elif letter in answer:
            guessed += correct_letter(letter)
            wordle_pattern.append(SQUARES["correct_letter"])
        else:
            guessed += incorrect_letter(letter)
            wordle_pattern.append(SQUARES["incorrect_letter"])
    return "".join(guessed), "".join(wordle_pattern)


def game(console, word_chosen):
    already_guessed, full_wordle_pattern, all_words_guessed = [], [], []

    while True:
        guess = Prompt.ask("\nEnter your guess").upper()
        while len(guess) != 5 or guess in already_guessed:
            if guess in already_guessed: console.print("[red]You've already guessed this word!!\n[/]")
            else: console.print("[red]Please enter a 5-letter word!!\n[/]")
            guess = Prompt.ask("\nEnter your guess").upper()
        already_guessed.append(guess)
        guessed, pattern = check_guess(guess, word_chosen)
        all_words_guessed.append(guessed)
        full_wordle_pattern.append(pattern)

        console.print(*all_words_guessed, sep="\n")
        if guess == word_chosen or len(already_guessed) == MAX_GUESSES: break
    if len(already_guessed) == MAX_GUESSES and guess != word_chosen:
        console.print(f"\n[red]WORDLE X/{MAX_GUESSES}[/]")
        console.print(f"\n[green]Correct Word: {word_chosen}[/]")
    else:
        console.print(f"\n[green]WORDLE {len(already_guessed)}/{MAX_GUESSES}[/]\n")
    console.print(*full_wordle_pattern, sep="\n")


if __name__ == "__main__":
    console = Console()
    word_chosen = choice(word_list)
    console.print(f"\n[white on blue] WELCOME TO WORDLE [/]\n")
    console.print("You may start guessing\n")
    game(console, word_chosen)