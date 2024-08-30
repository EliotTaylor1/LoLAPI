import logging
import argparse

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
from src.database import Database


def configure_logging(level):
    logging.basicConfig(level=level)
    logger = logging.getLogger()
    logger.setLevel(level)


def main():
    db = Database()
    db.create_tables()
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
        db.close_connection()
        print("goodbye")
    else:
        raise Exception("Invalid user credentials")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LoL Account Info Viewer")
    parser.add_argument(
        '--log-level',
        type=str,
        default='CRITICAL',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level'
    )
    args = parser.parse_args()
    configure_logging(args.log_level)

    try:
        main()
    except Exception as e:
        print(e)
