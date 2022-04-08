from random import choice, shuffle


LOWERCASE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z']
UPPERCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def generate_password(lowercase: bool, uppercase: bool, number: bool, custom_chars: str, required_length: int) -> str:
    temp_password: str = ""
    if lowercase:
        temp_password += choice(LOWERCASE_LETTERS)
    if uppercase:
        temp_password += choice(UPPERCASE_LETTERS)
    if number:
        temp_password += choice(NUMBERS)
    if len(custom_chars) > 0:
        temp_password += choice(custom_chars)
    while len(temp_password) < required_length:
        temp_password += generate_next_char(lowercase, uppercase, number, custom_chars)
    character_list = []
    character_list[:0] = temp_password
    shuffle(character_list)

    return "".join(character_list)


def generate_next_char(lowercase: bool, uppercase: bool, number: bool, custom_chars: str) -> chr:
    has_custom_char = len(custom_chars) > 0
    type_list = ""
    # Lowercase letters have much higher weight
    if lowercase:
        type_list += "LLLLLLLLLL"
    if uppercase:
        type_list += "UUUUU"
    if number:
        type_list += "NNN"
    if has_custom_char:
        type_list += "C"
    random_type = choice(type_list)
    if random_type == "U":
        return choice(UPPERCASE_LETTERS)
    elif random_type == "N":
        return choice(NUMBERS)
    elif random_type == "C":
        return choice(custom_chars)
    else:
        return choice(LOWERCASE_LETTERS)


# -------------------- Test -------------------- #
def __generate_a_list_of_passwords():
    for i in range(20):
        result = generate_password(lowercase=True, uppercase=True, number=True, custom_chars="@#", required_length=8)
        print(result)


# __generate_a_list_of_passwords()

