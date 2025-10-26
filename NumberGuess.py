import random
turn = 5
guess = 0
number = random.randrange(25) + 1
print("The computer is thinking of a number between 1 to 25. Try guessing it. You have 5 turns")


while guess != number and turn != 0:
    print("Turns Remaining: ", turn)
    guess = int(input("Guess a number: "))
    if guess < number and turn != 1:
        print("Guess a greater number.")
    elif guess > number and turn != 1:
        print("Guess a lower number.")

    turn = turn - 1

if guess == number:
    print("Congratulations! You won!")
if turn == 0 and guess != number:
    print("Sorry! You ran out of turns. The computer guessed: ", number)
