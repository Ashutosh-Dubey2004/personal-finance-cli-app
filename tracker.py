import datetime
import sqlite3

from ui_utils import clear, banner, pause, choose_category, CATEGORIES
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

        category = choose_category()
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
            SELECT id, amount, type, category, note, date 
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
                print(f"{row[5]} | ID: {row[0]} | ₹{row[1]:.2f} | {row[2].capitalize()} | {row[3]} | Note: {row[4]}")
    except Exception as e:
        print(f" Error retrieving transactions: {e}")
    finally:
        pause()

def deleteTransaction(user_id):
    clear()
    viewTransaction(user_id)

    try:
        tid = int(input("\nEnter the Transaction ID to edit: "))
    except ValueError:
        print("Invalid ID format.")
        return
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM transactions
            WHERE id = ? AND user_id = ?
        """, (tid, user_id,))
        row = cursor.fetchall()

        if not row:
            print("No transactions found.")
        else:
            confirm = input("Are you sure you want to delete this transaction? (yes/no): ").lower()

            if confirm == "yes":
                cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (tid, user_id))
                conn.commit()
                print("Transaction deleted successfully.")
            else:
                print("Deletion cancelled.")

    except Exception as e:
        print(f" Error retrieving transactions: {e}")
    finally:
        conn.close()
        pause()

def editTransaction(user_id):
    clear()
    viewTransaction(user_id)

    try:
        tid = int(input("\nEnter the Transaction ID to edit: "))
    except ValueError:
        print("Invalid ID format.")
        return
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM transactions
            WHERE id = ? AND user_id = ?
        """, (tid, user_id,))
        row = cursor.fetchone()

        if not row:
            print("No transactions found.")
        else:
                print("\nLeave blank to keep current value.\n")

                new_amount = input(f"New Amount (₹{row[2]}): ")
                new_type = input(f"New Type [{row[3]}] (income/expense): ").lower()
                new_category = input(f"New Category [{row[4]}] - {CATEGORIES}: ") or row[4]
                new_note = input(f"New Note [{row[5]}]: ")
                new_date = input(f"New Date [{row[6]}] (YYYY-MM-DD): ")

                updated_values = {
                    "amount": float(new_amount) if new_amount else row[2],
                    "type": new_type if new_type in ['income', 'expense'] else row[3],
                    "category": new_category if new_category else row[4],
                    "note": new_note if new_note else row[5],
                    "date": new_date if new_date else row[6]
                }

                try:
                    datetime.strptime(updated_values["date"], "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format.")
                    return

                cursor.execute('''
                    UPDATE transactions
                    SET amount = ?, type = ?, category = ?, note = ?, date = ?
                    WHERE id = ? AND user_id = ?
                ''', (updated_values["amount"], updated_values["type"], updated_values["category"],
                    updated_values["note"], updated_values["date"], tid, user_id))

                conn.commit()

    except Exception as e:
        print(f" Error retrieving transactions: {e}")
    finally:
        conn.close()
        pause()