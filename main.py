from db_init import initDB, initTransactionsTable
from ui_utils import banner, clear, pause
from auth import register, login
from tracker import addTransaction, viewTransaction, deleteTransaction, editTransaction
from report import generateFinancialReport
def mainMenu():
    while True:
        try:
            banner("Personal Finance Manager")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                register()
                clear()

            elif choice == '2':
                userId = login()
                clear()

                if userId:
                    while True:
                        try:
                            banner("Dashboard")
                            print("1. Add Transaction")
                            print("2. View Transactions")
                            print("3. Edit Transactions")
                            print("4. Delete Transactions")
                            print("5. Generate Financial Report")
                            print("6. Logout")

                            choice = input("Enter Choice: ").strip()

                            if choice == "1":
                                addTransaction(userId)
                                clear()
                            elif choice == "2":
                                viewTransaction(userId)
                                clear()
                            elif choice == "3":
                                editTransaction(userId)
                                clear()
                            elif choice == "4":
                                deleteTransaction(userId)
                                clear()
                            elif choice == "5":
                                generateFinancialReport(userId)
                                clear()
                            elif choice == "6":
                                print("Logging out...")
                                pause()
                                clear()
                                break
                            else:
                                pause("Invalid choice. Please try again.")
                        except Exception as e:
                            pause(f"Error: {str(e)}")

            elif choice == '3':
                print("Exiting the program.")
                break
            else:
                pause("Invalid option. Please choose 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            pause(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    initDB()
    initTransactionsTable()
    mainMenu()