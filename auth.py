import sqlite3
from passlib.hash import bcrypt

import ui_utils

DB_NAME = "finance.db"

def initDB():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register():
    ui_utils.clear()
    ui_utils.banner("Register New User")

    while True:
        username = input(" Enter a username: ").strip()
        if not username:
            print(" Username cannot be empty. Please try again.\n")
            continue

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(" Username already exists. Please choose a different one.\n")
            conn.close()
            continue
        conn.close()
        break

    while True:
        password = ui_utils.get_password(" Enter a password: ")
        if not password:
            print(" Password cannot be empty. Please try again.\n")
            continue
        break

    hashed_password = bcrypt.hash(password)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("\n Registration successful! You can now log in.")
    except Exception as e:
        print(f" Error: {e}")
    finally:
        conn.close()
        ui_utils.pause()

def login():
    ui_utils.clear()
    ui_utils.banner("User Login")

    username = input(" Username: ").strip()
    if not username:
        print(" Username cannot be empty.")
        ui_utils.pause()
        return False

    password = ui_utils.get_password(" Password: ")
    if not password:
        print(" Password cannot be empty.")
        ui_utils.pause()
        return False

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.verify(password, row[0]):
        print(f"\n Welcome back, {username}!")
        ui_utils.pause()
        return True
    else:
        print(" Invalid username or password.")
        ui_utils.pause()
        return False
    
if __name__ == "__main__":
    # initDB()
    # register()
    login()