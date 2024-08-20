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
