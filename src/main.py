from riot_account import RiotAccount
from match import Match

game_name = input("Enter ign: ")
tagline = input("Enter tag: ")
num_of_games_input = input("Enter number of games: ")
num_of_games = int(num_of_games_input)


def main():
    if type(game_name) is not str:
        raise TypeError(f"Name must be a string")
    elif type(tagline) is not str:
        raise TypeError(f"Tag must be a string")
    elif type(num_of_games) is not int:
        raise TypeError(f"Number of games must be int")
    else:
        account = RiotAccount(game_name, tagline, num_of_games)
        print(account.get_matches())
        print(account.get_matches()[0])


try:
    main()
except Exception as e:
    print(e)
