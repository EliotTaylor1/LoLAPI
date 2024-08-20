from src.menus import (
    print_main_menu,
    handle_match_history_submenu
)

from src.inputs import (
    get_user_input,
    is_tag_valid,
    is_account_name_valid
)

from src.riot_account import RiotAccount


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

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
