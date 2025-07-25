import sqlite3
import os
import msvcrt
from passlib.hash import bcrypt

def initDB():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
                   )
        ''')
    cursor.close()

def getPassword(prompt="Password: "):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:  # Enter
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
    return password


def register():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n Register New User")
    username = input("Enter a username: ")
    password = getPassword("Enter a password: ")
    hashed = bcrypt.hash(password)
    
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
         print("Username already exists.")
    conn.close()

def login():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n Login")
    username = input("Username: ")
    password = getPassword("Password: ")

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.verify(password, row[0]):
        print(f"Welcome back, {username}!")
        return True
    else:
        print("Invalid credentials.")
        return False

if __name__ == "__main__":
    initDB()
    register()
    login()