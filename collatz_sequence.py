#  collatz_sequence.py


def collatz(number: int) -> int:
    while number != 1:
        if number % 2 == 0:
            number //= 2
        else:
            number = 3 * number + 1

        print(number, end=' ')
