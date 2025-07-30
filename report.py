from datetime import datetime
import sqlite3
from db_init import DB_NAME
from ui_utils import banner, pause

def generateFinancialReport(current_user_id):
    banner("Financial Report")
    print("1. Monthly Report")
    print("2. Yearly Report")
    option = input("Choose an option: ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if option == "1":
        month = input("Enter month (01 to 12): ").zfill(2)
        year = input("Enter year (e.g., 2025): ")
        if not (month.isdigit() and 1 <= int(month) <= 12 and year.isdigit()):
            print(" Invalid month or year input.")
            pause()
            return

        date_filter = f"{year}-{month}"
        cursor.execute("""
            SELECT type, amount FROM transactions 
            WHERE user_id = ? AND date LIKE ?
        """, (current_user_id, f"{date_filter}%",))

    elif option == "2":
        year = input("Enter year (e.g., 2025): ").strip()
        if not year.isdigit():
            print(" Invalid year input.")
            pause()
            return

        cursor.execute("""
            SELECT type, amount FROM transactions 
            WHERE user_id = ? AND date LIKE ?
        """, (current_user_id, f"{year}%",))
    
    else:
        print(" Invalid option selected.")
        pause()
        return

    rows = cursor.fetchall()

    if not rows:
        print("\n No transactions found for the selected period.")
        pause()
        return

    total_income = sum(amount for t_type, amount in rows if t_type.lower() == 'income')
    total_expense = sum(amount for t_type, amount in rows if t_type.lower() == 'expense')
    net_savings = total_income - total_expense

    print("\n Report Summary:")
    print(f" Total Income   : ₹{total_income:,.2f}")
    print(f" Total Expenses : ₹{total_expense:,.2f}")
    print(f" Net Savings    : ₹{net_savings:,.2f}")

    conn.close()
    pause()

def showMonthlySummary(current_user_id):
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, amount FROM transactions 
        WHERE user_id = ? AND date LIKE ?
    """, (current_user_id, f"{year}-{month}%",))

    rows = cursor.fetchall()

    if not rows:
        print("\nNo transactions found for current month.")
        conn.close()
        return

    total_income = sum(amount for t_type, amount in rows if t_type.lower() == 'income')
    total_expense = sum(amount for t_type, amount in rows if t_type.lower() == 'expense')
    net_savings = total_income - total_expense

    banner("Monthly Summary")
    print(f"Month: {month}-{year}")
    print(f"Total Income   : ₹{total_income:,.2f}")
    print(f"Total Expenses : ₹{total_expense:,.2f}")
    print(f"Net Savings    : ₹{net_savings:,.2f}")
    conn.close()

import csv

def exportTransactionsToCSV(current_user_id, filename='transactions_export.csv'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, type, category, amount, note 
        FROM transactions 
        WHERE user_id = ?
        ORDER BY date DESC
    """, (current_user_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nNo transactions available to export.")
        pause()
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Note'])  
            writer.writerows(rows)
        print(f"\n Transactions exported successfully to '{filename}'")
    except Exception as e:
        print(f" Error while exporting: {e}")
    pause()
