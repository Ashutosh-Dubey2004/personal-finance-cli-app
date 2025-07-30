import datetime
import sqlite3

from ui_utils import clear, banner, pause, choose_category, CATEGORIES
from db_init import DB_NAME

def addTransaction(userId):
    clear()
    banner("Add a New Transaction")

    try:
        while True:
            amountInput = input("Enter amount: ").strip()
            if not amountInput:
                print("Amount cannot be empty.")
                continue
            try:
                amount = float(amountInput)
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

        while True:
            transType = input("Type ('income' or 'expense'): ").strip().lower()
            if transType in ['income', 'expense']:
                break
            print("Invalid type. Please enter 'income' or 'expense'.")

        category = choose_category()
        note = input("Add a note (optional): ").strip()

        while True:
            dateInput = input("Enter date (YYYY-MM-DD) [leave empty for today]: ").strip()
            if not dateInput:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                break
            try:
                datetime.datetime.strptime(dateInput, "%Y-%m-%d")
                date = dateInput
                break
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (user_id, amount, type, category, note, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (userId, amount, transType, category, note, date))
        conn.commit()
        conn.close()

        print("\nTransaction added successfully.")
    except Exception as e:
        print(f"Error adding transaction: {e}")
    finally:
        pause()

def viewTransaction(userId):
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
        """, (userId,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No transactions found.")
        else:
            for row in rows:
                print(f"{row[5]} | ID: {row[0]} | ₹{row[1]:.2f} | {row[2].capitalize()} | {row[3]} | Note: {row[4]}")
    except Exception as e:
        print(f"Error retrieving transactions: {e}")
    finally:
        pause()

def deleteTransaction(userId):
    clear()
    viewTransaction(userId)

    try:
        tid = int(input("\nEnter the Transaction ID to delete: "))
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
        """, (tid, userId))
        row = cursor.fetchone()

        if not row:
            print("No transaction found.")
        else:
            confirm = input("Are you sure you want to delete this transaction? (yes/no): ").lower()

            if confirm == "yes":
                cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (tid, userId))
                conn.commit()
                print("Transaction deleted successfully.")
            else:
                print("Deletion cancelled.")

    except Exception as e:
        print(f"Error deleting transaction: {e}")
    finally:
        conn.close()
        pause()

def editTransaction(userId):
    clear()
    viewTransaction(userId)

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
        """, (tid, userId))
        row = cursor.fetchone()

        if not row:
            print("No transaction found.")
        else:
            print("\nLeave blank to keep current value.\n")

            newAmount = input(f"New Amount (₹{row[2]}): ")
            newType = input(f"New Type [{row[3]}] (income/expense): ").lower()
            newCategory = input(f"New Category [{row[4]}] - {CATEGORIES}: ") or row[4]
            newNote = input(f"New Note [{row[5]}]: ")
            newDate = input(f"New Date [{row[6]}] (YYYY-MM-DD): ")

            updatedValues = {
                "amount": float(newAmount) if newAmount else row[2],
                "type": newType if newType in ['income', 'expense'] else row[3],
                "category": newCategory if newCategory else row[4],
                "note": newNote if newNote else row[5],
                "date": newDate if newDate else row[6]
            }

            try:
                datetime.datetime.strptime(updatedValues["date"], "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                return

            cursor.execute("""
                UPDATE transactions
                SET amount = ?, type = ?, category = ?, note = ?, date = ?
                WHERE id = ? AND user_id = ?
            """, (
                updatedValues["amount"], updatedValues["type"], updatedValues["category"],
                updatedValues["note"], updatedValues["date"], tid, userId
            ))

            conn.commit()
            print("Transaction updated successfully.")

    except Exception as e:
        print(f"Error editing transaction: {e}")
    finally:
        conn.close()
        pause()

def searchTransaction(userId):
    clear()
    banner("Search Transactions")

    print("Leave any field empty to ignore that filter.\n")

    transType = input("Type to filter (income/expense): ").strip().lower()
    category = input(f"Category to filter ({CATEGORIES}): ").strip()
    startDate = input("Start Date (YYYY-MM-DD): ").strip()
    endDate = input("End Date (YYYY-MM-DD): ").strip()

    query = "SELECT id, amount, type, category, note, date FROM transactions WHERE user_id = ?"
    params = [userId]

    if transType in ['income', 'expense']:
        query += " AND type = ?"
        params.append(transType)

    if category:
        query += " AND category = ?"
        params.append(category)

    if startDate:
        query += " AND date >= ?"
        params.append(startDate)

    if endDate:
        query += " AND date <= ?"
        params.append(endDate)

    query += " ORDER BY date DESC"

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No matching transactions found.")
        else:
            for row in rows:
                print(f"{row[5]} | ID: {row[0]} | ₹{row[1]:.2f} | {row[2].capitalize()} | {row[3]} | Note: {row[4]}")
    except Exception as e:
        print(f"Error while searching: {e}")
    finally:
        pause()
