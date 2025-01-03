import random
import string


def generate_easy_password(length=12):
    lower = string.ascii_lowercase
    password = [
        random.choice(lower),
    ]

    all_characters = lower
    password += random.choices(all_characters, k=length - 4)

    random.shuffle(password)

    return ''.join(password)