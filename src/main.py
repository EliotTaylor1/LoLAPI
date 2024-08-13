from RiotAccount import RiotAccount

game_name = "Eiiot"
tagline = "EUW"


def main():
    account = RiotAccount(game_name, tagline)
    print(account)
    print(account.get_match_history(2))


main()
