import requests
from utils import BASE_URL, COURIER_CREATE, COURIER_LOGIN, COURIER_DELETE, HEADERS, TIMEOUT
 

class CourierClient:


    def __init__(self):
        self.base_url = BASE_URL

    #Метод создания курьера
    def create(self, login, password, first_name):
        url_create = f"{self.base_url}{COURIER_CREATE}"
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(url_create, json=payload, headers=HEADERS, timeout=TIMEOUT)
        return response
    
    # Метод авторизация курьера
    def login(self,login, password):
        url_login = f"{self.base_url}{COURIER_LOGIN}"
        payload = {"login": login, "password": password}
        response = requests.post(url_login, json=payload, headers=HEADERS, timeout=TIMEOUT)
        return response

    # Метод удаление курьера
    def delete(self, courier_id):
        url_delete = f"{self.base_url}{COURIER_DELETE}/{courier_id}"
        response = requests.delete(url_delete, headers=HEADERS, timeout=TIMEOUT)
        return response