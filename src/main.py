from src.riot_account import RiotAccount


def get_user_input():
    name = input("Enter account name: ")
    tag = input("Enter tag: ")
    return name, tag


def is_account_name_valid(name):
    if len(name) < 3 or len(name) > 16:
        print("Account name must be between 3 and 16 characters")
        return False
    else:
        return True


def is_tag_valid(tag):
    if tag[0] == '#':
        print("Tag should not start with #")
        return False
    elif len(tag) < 2 or len(tag) > 5:
        print("Tag must be between 2 - 5 characters")
        return False
    elif not tag.isalnum():
        print("Tag must only contain alphanumeric characters")
        return False
    else:
        return True


#if __name__ == "__main__":

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

def main():
    name, tag = get_user_input()
    if is_account_name_valid(name) and is_tag_valid(tag):
        account = RiotAccount(name, tag)
        while True:
            print_main_menu()
            user_input = int(input("Enter action number: "))
            if user_input == 1:
                print(f"\n{account}")
            elif user_input == 2:
                account.set_match_history_length()
                handle_match_history_submenu(account)
            elif user_input == 3:
                account.print_champion_mastery()
            elif user_input == 4:
                name, tag = get_user_input()
                if is_account_name_valid(name) and is_tag_valid(tag):
                    account = RiotAccount(name, tag)
                else:
                    raise Exception("Invalid user credentials")
            elif user_input == 5:
                break
            else:
                print("Invalid option chosen")
        print("goodbye")
    else:
        raise Exception("Invalid user credentials")

try:
    main()
except Exception as e:
    print(e)
