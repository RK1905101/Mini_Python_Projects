import hashlib
import requests
import re

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password too short. minimum of 8 characters is required")


    if re.search(r"[A-Z]", password):
        score += 1

    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1

    else:
        feedback.append(r"Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1

    else:
        feedback.append("Include at least one number.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    else:
        feedback.append("Add a special character (!@#$%, etc.)")

    if score >= 6:
        level = "Strong"
    elif score >= 4:
        level = "Mediam"
    else:
        level = "Weak"

    return level, feedback


def check_pwned(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    response = requests.get(url)
    if response.status_code != 200:
        return "Error checking breach data"
    
    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return f"Found in data breaches {count} times!"
        
    return "Not found in know breaches."


if __name__ == "__main__":
    pwd = input("Enter password to check: ")

    print("\nChecking password strength...")
    level, feedback = check_password_strength(pwd)
    print(f"Strength: {level}")
    if feedback:
        print("Suggestions:")
        for f in feedback:
            print(f" - {f}")

    print("\nChecking HaveIBeenPwned database...")
    print(check_pwned(pwd))
    