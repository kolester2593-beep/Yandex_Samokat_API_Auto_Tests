import pytest
import sys
import os

# НАСТРОЙКА ПУТЕЙ

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ИМПОРТЫ

from api import CourierClient, OrderClient
from models import Courier, Order
from utils import STATUS_OK, STATUS_NOT_FOUND


# ФИКСТУРЫ ДЛЯ КУРЬЕРОВ

# Возвращает экземпляр CourierClient.
# Используется в тестах, где нужно самостоятельно управлять запросами.
@pytest.fixture
def courier_client():
    yield CourierClient()


# Фикстура создаёт курьера перед тестом и удаляет после.
# Возвращает данные курьера и ответ на создание.
# Используется в тестах на успешное создание курьера.
@pytest.fixture
def created_courier(courier_client):
    courier = Courier()
    courier.generate()
    
    create_response = courier_client.create(
        courier.login,
        courier.password,
        courier.first_name
    )
    
    yield {
        'login': courier.login,
        'password': courier.password,
        'first_name': courier.first_name,
        'create_response': create_response
    }
    
    # Удаляем курьера
    try:
        login_response = courier_client.login(courier.login, courier.password)
        courier_id = login_response.json()["id"]
        courier_client.delete(courier_id)
    except:
        pass


# Фикстура для тестов на валидацию полей.
# Генерирует данные курьера, тест создаёт его в API,
@pytest.fixture
def courier_for_validation(courier_client):

    courier = Courier()
    courier.generate()
    
    yield {
        'login': courier.login,
        'password': courier.password,
        'first_name': courier.first_name
    }
    
    # Пытаемся удалить курьера (если тест его создал)
    try:
        login_response = courier_client.login(courier.login, courier.password)
        courier_id = login_response.json()["id"]
        courier_client.delete(courier_id)
    except:
        pass


# Фикстура создаёт курьера перед тестом и удаляет после.
# Возвращает данные курьера (login, password, first_name, id).
# Используется в тестах, где нужен существующий курьер (логин, дубликат, удаление).
#
@pytest.fixture
def new_courier():
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
    
    # Удаляем курьера
    try:
        courier_client.delete(courier_id)
    except:
        pass


# Фикстура создаёт курьера и сразу авторизует его.
# Возвращает данные + id из ответа на логин.
# Используется в тестах, где требуется авторизация.
@pytest.fixture
def authorized_courier():
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
    
    # Удаляем курьера
    try:
        courier_client.delete(courier_id)
    except:
        pass


# ФИКСТУРЫ ДЛЯ ЗАКАЗОВ


# Возвращает экземпляр OrderClient.
# Используется в тестах, где нужно самостоятельно управлять запросами.
@pytest.fixture
def order_client():
    yield OrderClient()


# Фикстура создаёт заказ перед тестом и удаляет после.
# Возвращает данные заказа и ответ на создание.
# Используется в тестах на успешное создание заказа.
@pytest.fixture
def created_order(order_client):
    order = Order()
    order.generate()
    
    create_response = order_client.create(order.to_dict())
    
    yield {
        'order_data': order.to_dict(),
        'create_response': create_response,
        'track': create_response.json()["track"]
    }
    
    # Отменяем заказ
    try:
        order_client.cancel(create_response.json()["track"])
    except:
        pass


# Фикстура для тестов на валидацию полей.
# Генерирует данные заказа, тест создаёт его в API
@pytest.fixture
def order_for_validation(order_client):
    order = Order()
    order.generate()
    
    order_data = order.to_dict()
    
    yield {
        'order_data': order_data
    }
    
    # Пытаемся отменить заказ (если тест его создал)
    try:
        # Получаем track из созданного заказа через список заказов
        # Или просто игнорируем, если заказ не создался (400)
        pass
    except:
        pass


# Фикстура создаёт новый заказ перед тестом.
# Возвращает данные заказа + track из ответа.
# Используется в тестах, где нужен существующий заказ (получение по треку, отмена).
@pytest.fixture
def new_order():
    order_client = OrderClient()
    order = Order()
    order.generate()
    
    create_response = order_client.create(order.to_dict())
    track = create_response.json()["track"]
    
    yield {
        'order_data': order.to_dict(),
        'track': track
    }
    
    # Отменяем заказ
    try:
        order_client.cancel(track)
    except:
        pass


# Фикстура создаёт курьера и заказ.
# Возвращает оба объекта для тестов accept/cancel.
# Используется в тестах принятия/отмены заказа.
@pytest.fixture
def order_with_courier():
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