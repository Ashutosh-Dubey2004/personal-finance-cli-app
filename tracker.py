import datetime
import sqlite3

from ui_utils import clear, banner, pause
from db_init import DB_NAME

def addTransaction(user_id):
    clear()
    banner("Add a New Transaction")

    try:
        while True:
            amount_input = input("Enter amount: ").strip()
            if amount_input == "":
                print("Amount cannot be empty.")
                continue
            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
                
        while True:
            trans_type = input("Type ('income' or 'expense'): ").strip().lower()
            if trans_type not in ['income', 'expense']:
                print("Invalid type. Please enter 'income' or 'expense'.")
                continue
            break

        while True:
            category = input("Enter category: ").strip()
            if category == "":
                print("Category cannot be empty.")
                continue
            break

        note = input("Add a note (optional): ").strip()

        while True:
            date = input("Enter date (YYYY-MM-DD) [leave empty for today]: ").strip()
            if date == "":
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                break
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, type, category, note, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, amount, trans_type, category, note, date))
        conn.commit()
        conn.close()

        print("\nTransaction added successfully!\n")
    except Exception as e:
        print(f" Error adding transaction: {e}")
    finally:
        pause()


def viewTransaction(user_id):
    clear()
    banner("Transaction History")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT amount, type, category, note, date 
            FROM transactions
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No transactions found.")
        else:
            for row in rows:
                print(f"{row[4]} | {row[1].title()} | ₹{row[0]:.2f} | {row[2]} | {row[3]}")
    except Exception as e:
        print(f" Error retrieving transactions: {e}")
    finally:
        pause()
