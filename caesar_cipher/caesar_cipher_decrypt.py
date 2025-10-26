#  caesar_cipher_decrypt.py
from string import ascii_letters, digits

CONTAINER = ascii_letters + digits


def decrypt(message: str, key=13) -> str:
    message_output = ""

    for letter in message:
        find_index = CONTAINER.index(letter)
        value = find_index - key

        if value < 0:
            value += len(CONTAINER)
            message_output += CONTAINER[value]
        else:
            message_output += CONTAINER[value]

    return message_output
