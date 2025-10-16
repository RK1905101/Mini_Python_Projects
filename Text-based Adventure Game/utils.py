from colorama import Fore, Style, init
init(autoreset=True)

def ctext(s: str, color: str = 'CYAN') -> str:
    col = getattr(__import__('colorama').Fore, color.upper(), Fore.CYAN)
    return f"{col}{s}{Style.RESET_ALL}"

ASCII_TITLE = r"""
           _                         _ 
     /\   | |                       | |
    /  \  | |__  _   _ ___ ___  __ _| |
   / /\ \ | '_ \| | | / __/ __|/ _` | |
  / ____ \| |_) | |_| \__ \__ \ (_| | |
 /_/    \_\_.__/ \__, |___/___/\__,_|_|
                  __/ |                
                 |___/                 
"""