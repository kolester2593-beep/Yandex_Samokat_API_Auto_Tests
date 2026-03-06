import pytest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from api import CourierClient, OrderClient
from models import Courier, Order
from utils import generate_random_string, generate_random_phone
from utils import STATUS_OK, STATUS_NOT_FOUND



@pytest.fixture
def new_courier(): # Фикстура создаёт нового курьера перед тестом и удаляет после. Возвращает данные курьера (login, password, first_name, id).
    courier_client = CourierClient()
    courier = Courier()
    courier.generate()
    
    create_response = courier_client.create(
        courier.login,
        courier.password,
        courier.first_name
    )
    
    login_response = courier_client.login(courier.login, courier.password)
    courier_id = login_response.json()["id"]
    
    yield {
        'login': courier.login,
        'password': courier.password,
        'first_name': courier.first_name,
        'id': courier_id
    }
    
    # удаляем курьера
    try:
        delete_response = courier_client.delete(courier_id)
        if delete_response.status_code not in [STATUS_OK, STATUS_NOT_FOUND]:
            raise Exception(f"Failed to delete courier: {delete_response.status_code}")
    except Exception as e:
        pass 


@pytest.fixture
def authorized_courier(): # Фикстура создаёт курьера и сразу авторизует его. Возвращает данные + id из ответа на логин.
    courier_client = CourierClient()
    courier = Courier()
    courier.generate()
    
    courier_client.create(
        courier.login,
        courier.password,
        courier.first_name
    )
    
    login_response = courier_client.login(courier.login, courier.password)
    courier_id = login_response.json()["id"]
    
    yield {
        'login': courier.login,
        'password': courier.password,
        'first_name': courier.first_name,
        'id': courier_id
    }
    
    try:
        courier_client.delete(courier_id)
    except:
        pass


@pytest.fixture
def courier_client():
    yield CourierClient()


@pytest.fixture
def new_order(): # Фикстура создаёт новый заказ перед тестом. Возвращает данные заказа + track из ответа.
    order_client = OrderClient()
    order = Order()
    order.generate()
    
    create_response = order_client.create(order.to_dict())
    track = create_response.json()["track"]
    
    yield {
        'order_data': order.to_dict(),
        'track': track
    }

    try:
        order_client.cancel(track)
    except:
        pass


@pytest.fixture
def order_with_courier(): # Фикстура создаёт курьера и заказ. Возвращает оба объекта для тестов accept/cancel.
    courier_client = CourierClient()
    order_client = OrderClient()
    
    # Создаём курьера
    courier = Courier()
    courier.generate()
    courier_client.create(
        courier.login,
        courier.password,
        courier.first_name
    )
    
    login_response = courier_client.login(courier.login, courier.password)
    courier_id = login_response.json()["id"]
    
    # Создаём заказ
    order = Order()
    order.generate()
    create_response = order_client.create(order.to_dict())
    track = create_response.json()["track"]
    
    # Получаем id заказа через трек
    get_response = order_client.get_by_track(track)
    order_id = get_response.json()["order"]["id"]
    
    yield {
        'courier_id': courier_id,
        'order_id': order_id,
        'track': track,
        'login': courier.login,
        'password': courier.password
    }
    
    try:
        courier_client.delete(courier_id)
    except:
        pass
    try:
        order_client.cancel(track)
    except:
        pass

@pytest.fixture
def order_client():
    yield OrderClient()

# Фикстура создаёт курьера перед тестом и удаляет после.
@pytest.fixture
def created_courier(courier_client):
    courier = Courier()
    courier.generate()
    
    create_response = courier_client.create(
        courier.login,
        courier.password,
        courier.first_name
    )
    
    # Возвращаем данные курьера и ответ на создание
    yield {
        'login': courier.login,
        'password': courier.password,
        'first_name': courier.first_name,
        'create_response': create_response
    }
    
    # Teardown: удаляем курьера
    login_response = courier_client.login(courier.login, courier.password)
    courier_id = login_response.json()["id"]
    
    try:
        courier_client.delete(courier_id)
    except:
        pass


#
@pytest.fixture 
def courier_for_validation(courier_client):
    # Генерируем данные (но не создаём в API)
    courier = Courier()
    courier.generate()
    
    login = courier.login
    password = courier.password
    first_name = courier.first_name
    
    # Отдаём данные тесту
    yield {
        'login': login,
        'password': password,
        'first_name': first_name
    }
    
    # Teardown: удаляем курьера (тест уже создал его)
    try:
        login_response = courier_client.login(login, password)
        courier_id = login_response.json()["id"]
        courier_client.delete(courier_id)
    except:
        pass  # Курьер мог не создаться (ошибка валидации)