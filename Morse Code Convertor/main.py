import time
import winsound
import os
from assets import logo, alp_to_code_dict, code_to_alp_dict


def sound_generated_code(code):
    frequency = 1000
    duration = 500
    for char in code:
        if char == ".":
            winsound.Beep(frequency, duration)
        else:
            time.sleep(1)


def code_decoder(code_text, decode_direction):
    decode_text = ""

    for char in code_text:
        try:
            if decode_direction == 'd':
                decode_text += f"{code_to_alp_dict[char]} "
            else:
                decode_text += f"{alp_to_code_dict[char]} "
        except KeyError:
            print("Enter a valid code to decode!!")
            break

    if decode_direction == 'c':
        coded_type = input(
            "Do you want audio generated morse code or text generated?Enter 'a' for audio and anything else for text: ")
        if coded_type in ['a', 'audio']:
            sound_generated_code(decode_text)

    return f"Decoded text: {decode_text}"


game_continue = True
while game_continue:
    os.system('cls')
    print(logo)
    print("Welcome to Morse Code Convertor\n")
    decode_direction = input("Enter 'd' for decoding a morse code or 'c' for generating a morse code: ").lower()
    if decode_direction not in ['c', 'd']:
        print("Wrong Input Try Again!!!")
        continue
    else:
        code_text = input("Enter the Code Text: ").upper()
        decoded_text = code_decoder(code_text, decode_direction)
        print(decoded_text)
    should_continue = input("\nDo you wish to continue? Type 'y' to continue, 'n' to exit: ").lower()
    if should_continue in ['yes', 'y']:
        game_continue = True
    elif should_continue in ['no', 'n']:
        game_continue = False
    else:
        should_continue = input("\nWrong Input Try Again!! Type 'y' to continue, 'n' to exit: ").lower()
