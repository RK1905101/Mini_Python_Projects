import os
import ast
import random
import sys
from colorama import init, Fore, Style
init(autoreset=True)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

POETIC_MAP = {
    "FunctionDef": ["creation", "genesis", "naming"],
    "For": ["circles", "repetition", "eternal motion"],
    "If": ["choice", "uncertainty", "fate divides"],
    "While": ["waiting", "persistence", "stillness"],
    "Try": ["risk", "hope", "fragility"],
    "ExceptHandler": ["failure", "grace", "redemption"],
    "Import": ["connection", "influence", "new light"],
    "Return": ["ending", "completion", "homecoming"],
    "With": ["unity", "collaboration", "silence"]
}

def extract_summary(filename):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
    node_types = [type(node).__name__ for node in ast.walk(tree)]
    return ", ".join(sorted(set(node_types)))

def local_haiku(summary):
    words = []
    for token in summary.split(", "):
        if token in POETIC_MAP:
            words.extend(POETIC_MAP[token])
    if not words:
        words = ["silence", "emptiness", "void"]

    lines = [
        f"{random.choice(words)} drifts in loops,",
        f"{random.choice(words)} whispers of {random.choice(words)},",
        f"code breathes softly still."
    ]
    return "\n".join(lines)

def gemini_haiku(summary):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "Write a 3-line haiku describing this Python code structure. "
            "Use minimal, elegant language, rhyming words and a hint of funny phrases:\n" + summary
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return None

def colorful_print(text):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
    for line in text.split("\n"):
        print(random.choice(colors) + line + Style.RESET_ALL)

def main():
    if len(sys.argv) < 2:
        print("usage: python codehaiku.py example_code.py")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        sys.exit(1)

    summary = extract_summary(filename)

    print("\n Your Code Haiku \n")

    poem = None
    if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
        poem = gemini_haiku(summary)

    if not poem:
        poem = local_haiku(summary)

    colorful_print(poem)

if __name__ == "__main__":
    main()
