import auth

def mainMenu():
    auth.initDB()
    while True:
        print("\n===== Personal Finance Manager =====")
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
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    mainMenu()