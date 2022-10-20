#  caesar_cipher_encrypt.py
from string import ascii_letters, digits

CONTAINER = ascii_letters + digits


def encrypt(message: str, key=13) -> str:
    message_output = ""

    for letter in message:
        find_index = CONTAINER.index(letter)
        value = find_index + key
        if value > len(CONTAINER):
            value -= len(CONTAINER)
            message_output += CONTAINER[value]
        else:
            message_output += CONTAINER[value]

    return message_output
