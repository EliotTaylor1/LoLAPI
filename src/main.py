from RiotAccount import RiotAccount
from match import Match

game_name = "Eiiot"
tagline = "EUW"


def main():
    account = RiotAccount(game_name, tagline)
    print(account)
    account.get_match_history(2)
    match = Match(account.matches[0])
    print(match)

main()
