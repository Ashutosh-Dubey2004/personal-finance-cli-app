import os
import time
import msvcrt
from colorama import Fore, Style, init

init(autoreset=True)  

CATEGORIES = ['Food', 'Rent', 'Salary', 'Transport', 'Health', 'Entertainment', 'Utilities', 'Other']

def choose_category():
    print(Fore.CYAN + "\nSelect a Category:" + Style.RESET_ALL)
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    while True:
        try:
            choice = int(input("Enter your choice (1–{}): ".format(len(CATEGORIES))))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            else:
                print(Fore.RED + "Invalid choice. Please select a valid number.")
        except ValueError:
            print(Fore.RED + "Please enter a number.")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Press Enter to continue..."):
    input(Fore.YELLOW + msg + Style.RESET_ALL)

def banner(title):
    line = "=" * 50
    print("\n" + Fore.CYAN + line)
    print(Fore.WHITE + title.upper().center(50))
    print(Fore.CYAN + line + Style.RESET_ALL + "\n")


def wait(seconds=1):
    time.sleep(seconds)

def get_password(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print('')
            break
        elif ch == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        elif ch == b'\x03':  # Ctrl+C
            raise KeyboardInterrupt
        else:
            try:
                char = ch.decode('utf-8')
                password += char
                print('*', end='', flush=True)
            except UnicodeDecodeError:
                continue
    return password.strip()

def footer():
    print(Fore.MAGENTA + "-" * 50)
    print("Built with 💙 by Ashutosh Dubey".center(50))
    print("-" * 50 + Style.RESET_ALL)
