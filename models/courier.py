import random
import string


class Courier:

    def __init__(self, login=None, password=None, first_name=None):
        self.login = login
        self.password = password
        self.first_name = first_name
        
    # Метод преобразование в словарь
    def to_dict(self):
        return {
            "login": self.login,
            "password": self.password,
            "firstName": self.first_name
        }
    
    # Метод генерация случайных данных
    def generate(self, length=10):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for _ in range(length))
            return random_string
        
        self.login = generate_random_string(length)
        self.password = generate_random_string(length)
        self.first_name = generate_random_string(length)
        
        return self
