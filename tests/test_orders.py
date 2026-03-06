import pytest
import allure
from utils import STATUS_CREATED, STATUS_OK, STATUS_BAD_REQUEST, STATUS_NOT_FOUND, ERROR_INSUFFICIENT_DATA
from models import Order


@allure.feature("Orders")
class TestOrderCreate:

    @allure.story("Create order")
    @allure.title("Успешное создание заказа")
    @pytest.mark.parametrize("color,expected_status", [
        (["BLACK"], STATUS_CREATED),
        (["GREY"], STATUS_CREATED),
        (["BLACK", "GREY"], STATUS_CREATED),
        (None, STATUS_CREATED),
    ])
    def test_create_order_with_different_colors(self, order_client, color, expected_status):
        order = Order()
        order.generate(color=color)
        order_data = order.to_dict()
        response = order_client.create(order_data)
        assert response.status_code == expected_status
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
        assert response.json()["track"] > 0


    @allure.story("Create order")
    @allure.title("Проверка track в ответе")
    def test_create_order_response_contains_track(self, order_client):
        order = Order()
        order.generate()
        order_data = order.to_dict()
        response = order_client.create(order_data)
        assert response.status_code == STATUS_CREATED
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
        assert response.json()["track"] > 0


    @allure.story("Create order")
    @allure.title("Создание заказа: без обязательных полей")
    @allure.label('bug', 'true')
    @pytest.mark.xfail(reason="API не валидирует обязательные поля согласно документации")
    @pytest.mark.parametrize("missing_field", ("firstName", "phone", "lastName", "address", "metroStation", "rentTime", "deliveryDate"))
    def test_create_order_without_required_field(self, order_client, missing_field):
        order = Order()
        order.generate()
        order_data = order.to_dict()
        del order_data[missing_field]
        response = order_client.create(order_data)
        assert response.status_code == STATUS_BAD_REQUEST
        assert "message" in response.json()
        assert ERROR_INSUFFICIENT_DATA in response.json()["message"]


@allure.feature("Orders")
class TestOrderList:


    @allure.story("Get order list")
    @allure.title("Список заказов возвращается")
    def test_get_orders_list_success(self, order_client):
        response = order_client.get_list()
        assert response.status_code == STATUS_OK
        assert "orders" in response.json()


    @allure.story("Get order list")
    @allure.title("Пагинация работает (limit, page)")
    def test_get_orders_list_with_pagination(self, order_client):
        response = order_client.get_list(limit=5, page=1)
        assert "pageInfo" in response.json()
        assert response.json()["pageInfo"]["limit"] == 5
        assert response.json()["pageInfo"]["page"] == 1
    

    @allure.story("Get order list")
    @allure.title("Структура ответа (orders, pageInfo)")
    def test_get_orders_list_response_structure(self, order_client):
        response = order_client.get_list()
        assert "orders" in response.json()
        assert "pageInfo" in response.json()
        assert "availableStations" in response.json()
        assert isinstance(response.json()["orders"], list)


@allure.feature("Orders")
class TestOrderByTrack:


    @allure.story("Get order by track")
    @allure.title("Заказ по треку найден")
    def test_get_order_by_track_success(self, order_client, new_order):
        response = order_client.get_by_track(new_order['track'])
        assert response.status_code == STATUS_OK
        assert "order" in response.json()


    @allure.story("Get order by track")
    @allure.title("Без параметра t")
    def test_get_order_by_track_without_param(self, order_client):
        response = order_client.get_by_track(None)
        assert response.status_code == STATUS_BAD_REQUEST


    @allure.story("Get order by track")
    @allure.title("Несуществующий трек")
    def test_get_order_by_track_nonexistent(self, order_client):
        response = order_client.get_by_track(999999)
        assert response.status_code == STATUS_NOT_FOUND


@allure.feature("Orders")
class TestOrderAccept:


    @allure.story("Accept order")
    @allure.title("Успешное принятие")
    def test_accept_order_success(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        courier_id = order_with_courier['courier_id']
        response = order_client.accept(order_id, courier_id)
        assert response.status_code == STATUS_OK
        assert response.json()["ok"] is True


    @allure.story("Accept order")
    @allure.title("Нет courierId")
    def test_accept_order_without_courier_id(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        response = order_client.accept(order_id, None)
        assert response.status_code == STATUS_BAD_REQUEST

    
    @allure.story("Accept order")
    @allure.title("Нет order_id в URL")
    @pytest.mark.xfail(reason="API возвращает 500 вместо 400 при отсутствии order_id в URL")
    @allure.label('bug', 'true')
    def test_accept_order_without_order_id(self,order_client):
        courier_id = 123
        response = order_client.accept(None, courier_id)
        assert response.status_code == STATUS_BAD_REQUEST


    @allure.story("Accept order")
    @allure.title("Несуществующий заказ")
    def test_accept_order_nonexistent_order(self, order_with_courier, order_client):
        courier_id = order_with_courier['courier_id']
        nonexistent_order_id = 999999
        response = order_client.accept(nonexistent_order_id, courier_id)
        assert response.status_code == STATUS_NOT_FOUND


    @allure.story("Accept order")
    @allure.title("Несуществующий курьер")
    def test_accept_order_nonexistent_courier(self, order_with_courier, order_client):
        order_id = order_with_courier['order_id']
        nonexistent_courier_id = 999999999
        response = order_client.accept(order_id, nonexistent_courier_id)
        assert response.status_code == STATUS_NOT_FOUND
    

@allure.feature("Orders")
class TestOrderCancel:


    @allure.story("Cancel order")
    @allure.title("Успешная отмена")
    def test_cancel_order_success(self, new_order, order_client):
        track = new_order['track']
        response = order_client.cancel(track)
        assert response.status_code == STATUS_OK
        assert response.json()["ok"] is True

    @allure.story("Cancel order")
    @allure.title("Без параметра track")
    def test_cancel_order_without_track(self, order_client):
        response = order_client.cancel(None)
        assert response.status_code == STATUS_BAD_REQUEST


    @allure.story("Cancel order")
    @allure.title("Несуществующий трек")
    def test_cancel_order_nonexistent(self, order_client):
        track = 999999
        response = order_client.cancel(track)
        assert response.status_code == STATUS_NOT_FOUND