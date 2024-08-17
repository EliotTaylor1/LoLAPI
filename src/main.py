from riot_account import RiotAccount

name_valid = False
while not name_valid:
    name = input("Enter account name: ")
    if len(name) < 3 or len(name) > 16:
        print("Account name must be between 3 and 16 characters")
    else:
        name_valid = True

tag_valid = False
while not tag_valid:
    tag = input("Enter tag: ")
    if tag[0] == '#':
        print("Tag should not start with #")
    elif len(tag) < 2 or len(tag) > 5:
        print("Tag must be between 2 - 5 characters")
    elif not tag.isalnum():
        print("Tag must only contain alphanumeric characters")
    else:
        tag_valid = True


def print_main_menu():
    print("\nAvailable actions")
    print("1. Retrieve match history")
    print("2. View match history")
    print("3. Retrieve champion stats")
    print("4. Exit")


def print_match_history_menu():
    print("Available actions")
    print("1. Get match details")
    print("2. View match history")
    print("3. Return to main menu")


def handle_match_history_submenu(account):
    while True:
        print_match_history_menu()
        choice = int(input("Enter action number: "))
        if choice == 1:
            print("Enter match number to view")
            match_number = int(input("Match number: ")) - 1  # account for zero indexing
            if match_number < 0 or match_number > len(account.get_match_history()):
                print("Invalid match number")
            else:
                print("\n====== Match details ======")
                account.get_match_history()[match_number].print_detailed_match_stats()
        elif choice == 2:
            account.print_match_history()
        elif choice == 3:
            break
        else:
            print("Invalid action chosen")


def main():
    account = RiotAccount(name, tag)
    print(f"\n{account}")
    while True:
        print_main_menu()
        user_input = int(input("Enter action number: "))
        if user_input == 1:
            account.set_match_history_length()
        elif user_input == 2:
            account.print_match_history()
            handle_match_history_submenu(account)
        elif user_input == 3:
            raise NotImplementedError("WIP")
        elif user_input == 4:
            break
        else:
            print("Invalid option chosen")
    print("goodbye")


try:
    main()
except Exception as e:
    print(e)
