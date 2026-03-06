import requests
from utils import BASE_URL, ORDER_CREATE, ORDER_LIST, ORDER_BY_TRACK, ORDER_ACCEPT, ORDER_CANCEL, ORDER_FINISH, HEADERS, TIMEOUT


class OrderClient:

    def __init__(self):
        self.base_url = BASE_URL

    # Метод создание заказа
    def create(self, order_data):
        url_create = f"{self.base_url}{ORDER_CREATE}"
        response = requests.post(url_create, json=order_data, headers=HEADERS, timeout=TIMEOUT)
        return response
    
    # Метод получение списка заказов  
    def get_list(self, limit=None, page=None, courier_id=None):
        url_get_list = f"{self.base_url}{ORDER_LIST}"
        params = {}
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        if courier_id is not None:
            params["courierId"] = courier_id
        response = requests.get(url_get_list, params=params, headers=HEADERS, timeout=TIMEOUT)
        return response
    
    # Метод получение заказа по треку
    def get_by_track(self, track):
        url_get_list = f"{self.base_url}{ORDER_BY_TRACK}"
        params = {"t": track}
        response = requests.get(url_get_list, params=params, headers=HEADERS, timeout=TIMEOUT)
        return response

    # Метод принять заказ
    def accept(self, order_id, courier_id):
        url_accept = f"{self.base_url}{ORDER_ACCEPT}/{order_id}"
        params = {"courierId": courier_id}
        response = requests.put(url_accept, params=params, headers=HEADERS, timeout=TIMEOUT)
        return response
    
    # Метод отменить заказ
    def cancel(self, track):
        url_cancel = f"{self.base_url}{ORDER_CANCEL}"
        params = {"track": track}
        response = requests.put(url_cancel, params=params, headers=HEADERS, timeout=TIMEOUT)
        return response
