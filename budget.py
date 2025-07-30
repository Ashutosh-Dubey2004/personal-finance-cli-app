import sqlite3
from datetime import datetime
from db_init import DB_NAME
from ui_utils import CATEGORIES, pause

def setBudget(user_id):
    category = input(f"Enter category ({CATEGORIES})").strip()
    try:
        amount = float(input("Enter monthly budget amount: ").strip())
    except ValueError:
        print("Invalid amount.")
        return

    month = input("Enter month (YYYY-MM, default current): ").strip()
    if not month:
        month = datetime.now().strftime('%Y-%m')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, category, month)
        DO UPDATE SET amount = excluded.amount
    ''', (user_id, category, amount, month))

    conn.commit()
    conn.close()
    print(f"Budget of ₹{amount:.2f} set for {category} in {month}.")
    pause()

def viewBudgets(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category, amount, month FROM budgets
        WHERE user_id = ?
        ORDER BY month DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No budgets found.")
        return

    print("\nYour Budgets:")
    for category, amount, month in rows:
        print(f"{month} | {category}: ₹{amount:.2f}")
    
    pause()

def checkBudgetWarning(user_id):
    current_month = datetime.now().strftime('%Y-%m')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category, amount FROM budgets
        WHERE user_id = ? AND month = ?
    ''', (user_id, current_month))
    budgets = cursor.fetchall()

    for category, budget_amount in budgets:
        cursor.execute('''
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense'
              AND category = ? AND strftime('%Y-%m', date) = ?
        ''', (user_id, category, current_month))
        total_spent = cursor.fetchone()[0] or 0.0

        if total_spent > budget_amount:
            print(f"Budget exceeded in '{category}'. Spent: ₹{total_spent:.2f} / Budget: ₹{budget_amount:.2f}")
            pause()
            
    conn.close()
