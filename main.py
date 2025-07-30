from db_init import initializeAllTables
from ui_utils import banner, clear, pause, footer
from auth import register, login
from tracker import addTransaction, viewTransaction, deleteTransaction, editTransaction, searchTransaction
from report import generateFinancialReport
from budget import setBudget, viewBudgets, checkBudgetWarning
from backup import backupDatabase, restoreDatabase

def transactionMenu(userId):
    while True:
        clear()
        banner("Transactions & Budget")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Set Monthly Budget")
        print("6. View Budget Summary")
        print("7. Search Transactions")  
        print("8. Back to Dashboard")

        choice = input("Choose an option: ").strip()
        clear()

        if choice == "1":
            addTransaction(userId)
            checkBudgetWarning(userId)
        elif choice == "2":
            viewTransaction(userId)
        elif choice == "3":
            editTransaction(userId)
        elif choice == "4":
            deleteTransaction(userId)
        elif choice == "5":
            setBudget(userId)
        elif choice == "6":
            viewBudgets(userId)
        elif choice == "7":
            searchTransaction(userId)  
        elif choice == "8":
            break
        else:
            pause("Invalid choice.")

def reportsMenu(userId):
    while True:
        clear()
        banner("Reports & Tools")
        print("1. Generate Financial Report")
        print("2. Back to Dashboard")

        choice = input("Choose an option: ").strip()
        clear()

        if choice == "1":
            generateFinancialReport(userId)
        elif choice == "2":
            break
        else:
            pause("Invalid choice.")

def backupMenu():
    while True:
        clear()
        banner("Backup & Settings")
        print("1. Backup Data")
        print("2. Restore Data")
        print("3. Logout")

        choice = input("Choose an option: ").strip()
        clear()

        if choice == "1":
            backupDatabase()
        elif choice == "2":
            restoreDatabase()
        elif choice == "3":
            print("Logging out...")
            pause()
            break
        else:
            pause("Invalid choice.")

def dashboard(userId):
    while True:
        clear()
        banner("Dashboard")
        print("1. Transactions & Budget")
        print("2. Reports & Tools")
        print("3. Backup & Settings")

        choice = input("Choose an option: ").strip()
        clear()

        if choice == "1":
            transactionMenu(userId)
        elif choice == "2":
            reportsMenu(userId)
        elif choice == "3":
            backupMenu()
            break
        else:
            pause("Invalid choice.")

def mainMenu():
    while True:
        try:
            banner("Personal Finance Manager")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Choose an option: ").strip()
            clear()

            if choice == '1':
                register()
                clear()
            elif choice == '2':
                userId = login()
                clear()
                if userId:
                    dashboard(userId)
            elif choice == '3':
                print("Exiting the program.")
                footer()
                break
            else:
                pause("Invalid option. Please choose 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            pause(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    initializeAllTables()
    mainMenu()
