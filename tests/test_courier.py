import pytest
import allure
from utils import STATUS_CREATED, STATUS_OK, STATUS_BAD_REQUEST, STATUS_CONFLICT, STATUS_NOT_FOUND
import requests
from utils import BASE_URL, COURIER_CREATE,COURIER_DELETE, COURIER_LOGIN, HEADERS, TIMEOUT
from api import CourierClient
from models import Courier


@allure.feature("Courier")
class TestCourierCreate:

    @allure.story("Создание курьера: все данные")
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_data, courier_client):
        with allure.step("Отправка POST-запроса на создание курьера"):
            response = courier_client.create(
                courier_data['login'],
                courier_data['password'],
                courier_data['first_name']
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_CREATED
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True     


    @allure.story("Создание курьера: отсутствует логин")
    @allure.title("Создание без логина")
    def test_create_courier_without_login(self, courier_data, courier_client):
        payload = {
            "password": courier_data['password'],
            "firstName": courier_data['first_name']
        }
        with allure.step("Отправка POST-запроса на создание курьера без логина"):
            response = requests.post(
                f'{BASE_URL}{COURIER_CREATE}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Создание курьера: отсутствует пароль")
    @allure.title("Создание без пароля")
    def test_create_courier_without_password(self, courier_data, courier_client):
        payload = {
            "login": courier_data['login'],
            "firstName": courier_data['first_name']
        }
        with allure.step("Отправка POST-запроса на создание курьера без пароля"):
            response = requests.post(
                f'{BASE_URL}{COURIER_CREATE}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Создание курьера: отсутствует имя")
    @allure.title("Создание без имени")
    def test_create_courier_without_first_name(self, courier_data, courier_client):
        payload = {
            "login": courier_data['login'],
            "password": courier_data['password']
        }
        with allure.step("Отправка POST-запроса на создание курьера без имени"):
            response = requests.post(
                f'{BASE_URL}{COURIER_CREATE}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_CREATED
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True


    @allure.story("Создание курьера: дубликат логина")
    @allure.title("Дубликат логина")
    def test_create_duplicate_courier(self, courier_client, new_courier):
        with allure.step("Отправка POST-запроса на создание дубликата курьера"):
            response = courier_client.create(
                new_courier['login'],
                new_courier['password'],
                new_courier['first_name']
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_CONFLICT
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


@allure.feature("Login courier")
class TestCourierLogin:


    @allure.story("Авторизация: успешный вход")
    @allure.title("Успешный вход")
    def test_login_success(self, courier_client, authorized_courier):
        with allure.step("Отправка POST-запроса на авторизацию"):
            response = courier_client.login(
                authorized_courier['login'],
                authorized_courier['password']
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка наличия id в ответе"):
            assert "id" in response.json()
        with allure.step("Проверка типа id"):
            assert isinstance(response.json()["id"], int) 
        

    @allure.story("Авторизация: отсутствует логин")
    @allure.title("Отсутствует логин")
    def test_login_without_login(self, courier_data, courier_client):
        payload = {"password": courier_data['password']}
        with allure.step("Отправка POST-запроса на авторизацию без логина"):
            response = requests.post(
                f'{BASE_URL}{COURIER_LOGIN}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Авторизация: отсутствует пароль")
    @allure.title("Отсутствует пароль")
    @allure.label('bug', 'true')
    @pytest.mark.xfail(reason="API нестабилен: эндпоинт /login зависает без поля password")
    def test_login_without_password(self, new_courier, courier_client):
        payload = {"login": new_courier['login']}
        with allure.step("Отправка POST-запроса на авторизацию без пароля"):
            response = requests.post(
                f'{BASE_URL}{COURIER_LOGIN}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_BAD_REQUEST
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Авторизация: неверный пароль")
    @allure.title("Неверный пароль")
    def test_login_wrong_password(self, new_courier, courier_client):
        login = new_courier['login']
        wrong_password = "wrong_password_123"
        
        payload = {"login": login, "password": wrong_password}
        with allure.step("Отправка POST-запроса на авторизацию с неверным паролем"):
            response = requests.post(
                f'{BASE_URL}{COURIER_LOGIN}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Авторизация: несуществующий пользователь")
    @allure.title("Несуществующий пользователь")
    def test_login_nonexistent_user(self, courier_client):
        payload = {"login": "Trololo", "password": "123456789qwe"}
        with allure.step("Отправка POST-запроса на авторизацию несуществующего пользователя"):
            response = requests.post(
                f'{BASE_URL}{COURIER_LOGIN}',
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )
        with allure.step("Проверка наличия сообщения об ошибке"):
            response_data = response.json()
            assert "message" in response_data
            assert "не найдена" in response_data["message"]


@allure.feature("Delete courier")
class TestCourierDelete:


    @allure.story("Удаление курьера: успешное удаление")
    @allure.title("Успешное удаление")
    def test_delete_courier_success(self, new_courier, courier_client):
        courier_id = new_courier['id']
        with allure.step("Отправка DELETE-запроса на удаление курьера"):
            response = courier_client.delete(courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_OK
        with allure.step("Проверка тела ответа"):
            assert response.json()["ok"] is True
        
    
    @allure.story("Удаление курьера: отсутствует id")
    @allure.title("Удаление без id")
    def test_delete_without_id(self, courier_client):
        url = f'{BASE_URL}{COURIER_DELETE}'
        with allure.step("Отправка DELETE-запроса без id"):
            response = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Удаление курьера: несуществующий id")
    @allure.title("Удаление с несуществующим id")
    def test_delete_nonexistent_courier(self, courier_client):
        fake_courier_id = 99999999
        with allure.step("Отправка DELETE-запроса с несуществующим id"):
            response = courier_client.delete(fake_courier_id)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == STATUS_NOT_FOUND
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in response.json()


    @allure.story("Удаление курьера: проверка через авторизацию")
    @allure.title("После удаления курьер не может авторизоваться")
    def test_courier_cannot_login_after_delete(self, courier_client, new_courier):
        login = new_courier['login']
        password = new_courier['password']
        courier_id = new_courier['id']
        
        with allure.step("Отправка DELETE-запроса на удаление курьера"):
            courier_client.delete(courier_id)
        with allure.step("Отправка POST-запроса на авторизацию удалённого курьера"):
            login_response = courier_client.login(login, password)
        with allure.step("Проверка статуса ответа"):
            assert login_response.status_code == STATUS_NOT_FOUND
        with allure.step("Проверка наличия сообщения об ошибке"):
            assert "message" in login_response.json()
