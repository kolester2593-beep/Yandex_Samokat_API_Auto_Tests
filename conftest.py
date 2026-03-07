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
@pytest.fixture
def courier_client(): # Возвращает экземпляр CourierClient.
    yield CourierClient()


# Фикстура для тестов на СОЗДАНИЕ курьера.
# Генерирует данные, тест создаёт курьера, фикстура удаляет в teardown.
# НЕ создаёт курьера до теста! Иначе тест не проверяет создание.
@pytest.fixture
def courier_data(courier_client):
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
# Используется в тестах, где нужен СУЩЕСТВУЮЩИЙ курьер (логин, дубликат, удаление, принятие заказа).
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
# Переиспользует new_courier + добавляет логин.
# ИСПРАВЛЕНО: переиспользует new_courier вместо дублирования кода
# new_courier уже создал курьера и вернул данные
# Делаем логин и добавляем id к данным

@pytest.fixture
def authorized_courier(new_courier, courier_client):

    login_response = courier_client.login(new_courier['login'], new_courier['password'])
    courier_id = login_response.json()["id"]
    
    yield {
        'login': new_courier['login'],
        'password': new_courier['password'],
        'first_name': new_courier['first_name'],
        'id': courier_id
    }
    # new_courier сам удалит курьера


# ФИКСТУРЫ ДЛЯ ЗАКАЗОВ
@pytest.fixture
def order_client(): # Возвращает экземпляр OrderClient.
    yield OrderClient()


# Фикстура для тестов на СОЗДАНИЕ заказа.
# Генерирует данные, тест создаёт заказ, фикстура удаляет
# НЕ создаёт заказ до теста! Иначе тест не проверяет создание.
# Нужно получить track из созданного заказа
# Это сложно сделать без дополнительных запросов, поэтому оставляем пустым
# Тесты на валидацию (400) не создают заказ, cleanup не нужен


@pytest.fixture
def order_data(order_client):
    order = Order()
    order.generate()
    
    yield {
        'order_data': order.to_dict()
    }
    # Пытаемся отменить заказ (если тест его создал)
    try:

        pass
    except:
        pass


# Фикстура создаёт заказ перед тестом и удаляет после.
# Возвращает данные заказа и ответ на создание.
# Используется в тестах, где нужен СУЩЕСТВУЮЩИЙ заказ (получение по треку, отмена).
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


# Фикстура возвращает данные существующего заказа.
# ИСПРАВЛЕНО: переиспользует created_order вместо дублирования кода
@pytest.fixture
def new_order(created_order):
    yield {
        'order_data': created_order['order_data'],
        'track': created_order['track']
    }


# Фикстура создаёт курьера и заказ.
# ИСПРАВЛЕНО: переиспользует new_courier + created_order
@pytest.fixture
def order_with_courier(new_courier, created_order, order_client):
    # new_courier уже создал курьера
    courier_id = new_courier['id']
    # created_order уже создал заказ
    track = created_order['track']
    # Получаем id заказа через трек
    get_response = order_client.get_by_track(track)
    order_id = get_response.json()["order"]["id"]
    
    yield {
        'courier_id': courier_id,
        'order_id': order_id,
        'track': track,
        'login': new_courier['login'],
        'password': new_courier['password']
    }
    # new_courier и created_order сами удалят данные