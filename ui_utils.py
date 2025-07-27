import os
import time
import msvcrt

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg=" Press Enter to continue..."):
    input(msg)

def banner(title):
    print("=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40)

def wait(seconds=1):
    time.sleep(seconds)

def get_password(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:    # Enter
            print('')
            break
        elif ch == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        elif ch == b'\x03':
            raise KeyboardInterrupt
        else:
            try:
                char = ch.decode('utf-8')
                password += char
                print('*', end='', flush=True)
            except UnicodeDecodeError:
                continue
    return password.strip()
