import auth
import ui_utils

def mainMenu():
    auth.initDB()
    while True:
        ui_utils.banner("Personal Finance Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            auth.register()
        elif choice == '2':
            auth.login()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            ui_utils.pause("Invalid choice. Try again.")

if __name__ == "__main__":
    mainMenu()