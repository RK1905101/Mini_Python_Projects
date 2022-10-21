"""
This is a program that checks for strength of
password.
"""


def password_checker(password: str):
    if password.isalpha() and len(password) < 8:
        return f"The Password {password} is a very weak password."
    if password.isdecimal() and len(password) < 8:
        return f"The password {password} is a weak password."
    if password.isalnum() and len(password) >= 8:
        return f"The password {password} is a strong password."
    if password.isascii() and len(password) >= 8:
        return f"The password {password} is a very strong password."


print(password_checker('1337h@xor!'))
