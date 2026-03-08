import random
import string

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_phone():
    return "+7" + str(random.randint(1000000000, 9999999999))