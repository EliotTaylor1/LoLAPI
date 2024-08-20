def print_main_menu():
    print("\nAvailable actions")
    print("1. View profile information")
    print("2. View matches")
    print("3. Retrieve champion stats")
    print("4. Change account")
    print("5. Exit")


def print_match_history_menu():
    print("Available actions")
    print("1. View match history")
    print("2. Get match details")
    print("3. Change match history length")
    print("4. Return to main menu")


def handle_match_history_submenu(account):
    while True:
        print_match_history_menu()
        choice = int(input("Enter action number: "))
        if choice == 1:
            account.retrieve_match_history(account.get_match_history_length())
            account.print_match_history()
        elif choice == 2:
            print("Enter match number to view")
            match_number = int(input("Match number: ")) - 1  # account for zero indexing
            if match_number < 0 or match_number > len(account.get_match_history()):
                print("Invalid match number")
            else:
                print("\n====== Match details ======")
                account.get_match_history()[match_number].print_detailed_match_stats()
        elif choice == 3:
            account.reset_match_history()
            account.set_match_history_length()
        elif choice == 4:
            break
        else:
            print("Invalid action chosen")