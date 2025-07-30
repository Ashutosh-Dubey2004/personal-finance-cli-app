import sqlite3
from passlib.hash import bcrypt

import ui_utils
from db_init import DB_NAME
from report import showMonthlySummary  

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
    cursor.execute("SELECT id, password, login_count FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row and bcrypt.verify(password, row[1]):
        user_id = row[0]
        login_count = (row[2] or 0) + 1

        cursor.execute("UPDATE users SET login_count = ? WHERE id = ?", (login_count, user_id))
        conn.commit()
        conn.close()

        print(f"\n Welcome back, {username}!")

        showMonthlySummary(user_id)

        if login_count % 10 == 0:
            print("\n You haven't backed up in a while.")
            choice = input(" Do you want to create a backup now? (Y/N): ").strip().lower()
            if choice == 'y':
                from backup import create_backup
                create_backup(user_id)

        ui_utils.pause()
        return user_id
    else:
        conn.close()
        print(" Invalid username or password.")
        ui_utils.pause()
        return False

if __name__ == "__main__":
    login()
