import random
import string


class Order:

    def __init__(
        self,
        first_name=None,
        last_name=None,
        address=None,
        metro_station=None,
        phone=None,
        rent_time=None,
        delivery_date=None,
        comment=None,
        color=None
    ):

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.metro_station = metro_station
        self.phone = phone
        self.rent_time = rent_time
        self.delivery_date = delivery_date
        self.comment = comment
        self.color = color

    # Метод преобразование в словарь
    def to_dict(self):
        result = {}
        
        if self.first_name is not None:
            result["firstName"] = self.first_name
        if self.last_name is not None:
            result["lastName"] = self.last_name
        if self.address is not None:
            result["address"] = self.address
        if self.metro_station is not None:
            result["metroStation"] = self.metro_station
        if self.phone is not None:
            result["phone"] = self.phone
        if self.rent_time is not None:
            result["rentTime"] = self.rent_time
        if self.delivery_date is not None:
            result["deliveryDate"] = self.delivery_date
        if self.comment is not None:
            result["comment"] = self.comment
        if self.color is not None:
            result["color"] = self.color
        
        return result

    # Метод генерация случайных данных
    def generate(self, color=None):
        def generate_random_string(length=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for _ in range(length))
        
        def generate_random_phone():
            return "+7" + str(random.randint(1000000000, 9999999999))
        
        # Заполняем обязательные поля
        self.first_name = generate_random_string(10)
        self.last_name = generate_random_string(10)
        self.address = generate_random_string(20)
        self.metro_station = str(random.randint(1, 20))  
        self.phone = generate_random_phone()
        self.rent_time = random.randint(1, 10)  # дней аренды
        self.delivery_date = "2026-03-03"
        self.comment = generate_random_string(30)
        

        if color is None:
            self.color = ["BLACK"]  
        else:
            self.color = color
        
        return self