import pytest
import allure
from utils import STATUS_CREATED, STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND, ERROR_INSUFFICIENT_DATA
from utils import BASE_URL, ORDER_CREATE, HEADERS, TIMEOUT
import requests


@allure.feature("Create orders")
class TestOrderCreate:

    @allure.story("Создание заказа: разные цвета")
    @allure.title("Создание заказа с разными цветами")
    @pytest.mark.parametrize("color, expected_status", [
        (["BLACK"], STATUS_CREATED),
        (["GREY"], STATUS_CREATED),
        (["BLACK", "GREY"], STATUS_CREATED),
        (None, STATUS_CREATED),
    ])
    def test_create_order_with_different_colors(self, created_order, color, expected_status):
        create_response = created_order['create_response']
        with allure.step("Проверка статуса ответа"):
            assert create_response.status_code == expected_status
        with allure.step("Проверка наличия track в ответе"):
            assert "track" in create_response.json()
        with allure.step("Проверка типа track"):
            assert isinstance(create_response.json()["track"], int)
        with allure.step("Проверка значения track"):
            assert create_response.json()["track"] > 0


    @allure.story("Создание заказа: наличие track в ответе")
    @allure.title("Проверка наличия track в ответе")
    def test_create_order_response_contains_track(self, created_order):
        create_response = created_order['create_response']
        with allure.step("Проверка статуса ответа"):
            assert create_response.status_code == STATUS_CREATED
        with allure.step("Проверка наличия track в ответе"):
            assert "track" in create_response.json()
        with allure.step("Проверка типа track"):
            assert isinstance(create_response.json()["track"], int)
        with allure.step("Проверка значения track"):
            assert create_response.json()["track"] > 0


    @allure.story("Создание заказа: без обязательных полей")
    @allure.title("Создание без обязательных полей")
    @allure.label('bug', 'true')
    @pytest.mark.xfail(reason="API не валидирует обязательные поля согласно документации")
    @pytest.mark.parametrize("missing_field", ("firstName", "phone", "lastName", "address", "metroStation", "rentTime", "deliveryDate"))
    def test_create_order_without_required_field(self, order_for_validation, missing_field):
        order_data = order_for_validation['order_data']
        del order_data[missing_field]
        
        with allure.step("Отправка POST-запроса на создание заказа без поля"):
            response = requests.post(
                f'{BASE_URL}{ORDER_CREATE}',
                json=order_data,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()
        with allure.step("Проверка текста ошибки"):
            assert ERROR_INSUFFICIENT_DATA in response.json()["message"]


@allure.feature("List orders")
class TestOrderList:


    @allure.story("Список заказов: возвращается список")
    @allure.title("Получение списка заказов")
    def test_get_orders_list_success(self, order_client):
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = order_client.get_list()
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка наличия orders в ответе"):
            assert "orders" in response.json()


    @allure.story("Список заказов: пагинация работает")
    @allure.title("Проверка пагинации (limit, page)")
    def test_get_orders_list_with_pagination(self, order_client):
        with allure.step("Отправка GET-запроса с параметрами пагинации"):
            response = order_client.get_list(limit=5, page=1)
        with allure.step("Проверка наличия pageInfo в ответе"):
            assert "pageInfo" in response.json()
        with allure.step("Проверка значения limit"):
            assert response.json()["pageInfo"]["limit"] == 5
        with allure.step("Проверка значения page"):
            assert response.json()["pageInfo"]["page"] == 1
    

    @allure.story("Список заказов: структура ответа")
    @allure.title("Проверка структуры ответа")
    def test_get_orders_list_response_structure(self, order_client):
        with allure.step("Отправка GET-запроса на получение списка заказов"):
            response = order_client.get_list()
        with allure.step("Проверка наличия orders в ответе"):
            assert "orders" in response.json()
        with allure.step("Проверка наличия pageInfo в ответе"):
            assert "pageInfo" in response.json()
        with allure.step("Проверка наличия availableStations в ответе"):
            assert "availableStations" in response.json()
        with allure.step("Проверка типа orders"):
            assert isinstance(response.json()["orders"], list)


@allure.feature("By track orders")
class TestOrderByTrack:


    @allure.story("Заказ по треку: найден")
    @allure.title("Получение заказа по треку")
    def test_get_order_by_track_success(self, order_client, new_order):
        with allure.step("Отправка GET-запроса на получение заказа по треку"):
            response = order_client.get_by_track(new_order['track'])
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка наличия order в ответе"):
            assert "order" in response.json()


    @allure.story("Заказ по треку: несуществующий трек")
    @allure.title("Запрос с несуществующим треком")
    def test_get_order_by_track_nonexistent(self, order_client):
        with allure.step("Отправка GET-запроса с несуществующим треком"):
            response = order_client.get_by_track(999999)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND


    @allure.story("Заказ по треку: без параметра t")
    @allure.title("Запрос без параметра t")
    def test_get_order_by_track_without_param(self, order_client):
        with allure.step("Отправка GET-запроса без параметра t"):
            response = order_client.get_by_track(None)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST


@allure.feature("Accept orders")
class TestOrderAccept:


    @allure.story("Принять заказ: успешное принятие")
    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        courier_id = order_with_courier['courier_id']
        
        with allure.step("Отправка PUT-запроса на принятие заказа"):
            response = order_client.accept(order_id, courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True


    @allure.story("Принять заказ: нет courierId")
    @allure.title("Принятие без courierId")
    def test_accept_order_without_courier_id(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        
        with allure.step("Отправка PUT-запроса без courierId"):
            response = order_client.accept(order_id, None)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST

    
    @allure.story("Принять заказ: нет order_id в URL")
    @allure.title("Принятие без order_id")
    @allure.label('bug', 'true')
    @pytest.mark.xfail(reason="API возвращает 500 вместо 400 при отсутствии order_id в URL")
    def test_accept_order_without_order_id(self, order_client):
        courier_id = 123
        
        with allure.step("Отправка PUT-запроса без order_id"):
            response = order_client.accept(None, courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST


    @allure.story("Принять заказ: несуществующий заказ")
    @allure.title("Принятие несуществующего заказа")
    def test_accept_order_nonexistent_order(self, order_with_courier, order_client):
        courier_id = order_with_courier['courier_id']
        nonexistent_order_id = 999999
        
        with allure.step("Отправка PUT-запроса с несуществующим order_id"):
            response = order_client.accept(nonexistent_order_id, courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND


    @allure.story("Принять заказ: несуществующий курьер")
    @allure.title("Принятие с несуществующим курьером")
    def test_accept_order_nonexistent_courier(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        nonexistent_courier_id = 999999999
        
        with allure.step("Отправка PUT-запроса с несуществующим courier_id"):
            response = order_client.accept(order_id, nonexistent_courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND
    

@allure.feature("Cancel orders")
class TestOrderCancel:


    @allure.story("Отменить заказ: успешная отмена")
    @allure.title("Успешная отмена заказа")
    def test_cancel_order_success(self, new_order, order_client):
        track = new_order['track']
        
        with allure.step("Отправка PUT-запроса на отмену заказа"):
            response = order_client.cancel(track)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True


    @allure.story("Отменить заказ: без параметра track")
    @allure.title("Отмена без track")
    def test_cancel_order_without_track(self, order_client):
        with allure.step("Отправка PUT-запроса без track"):
            response = order_client.cancel(None)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST


    @allure.story("Отменить заказ: несуществующий трек")
    @allure.title("Отмена несуществующего заказа")
    def test_cancel_order_nonexistent(self, order_client):
        track = 999999
        
        with allure.step("Отправка PUT-запроса с несуществующим track"):
            response = order_client.cancel(track)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND