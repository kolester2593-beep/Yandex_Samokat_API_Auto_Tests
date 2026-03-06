import pytest
import allure
from utils import STATUS_CREATED, STATUS_OK, STATUS_BAD_REQUEST, STATUS_CONFLICT, STATUS_NOT_FOUND
import requests
from utils import BASE_URL, COURIER_CREATE,COURIER_DELETE, COURIER_LOGIN, HEADERS, TIMEOUT
from models import Courier


@allure.feature("Courier")
class TestCourierCreate:

    @allure.story("Создание курьера: все данные")
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, created_courier):
        create_response = created_courier['create_response']
        assert create_response.status_code == STATUS_CREATED
        assert create_response.json()["ok"] is True      


    @allure.story("Создание курьера: отсутствует логин")
    @allure.title("Создание без логина")
    def test_create_courier_without_login(self, courier_for_validation):
        password = courier_for_validation['password']
        first_name = courier_for_validation['first_name']
        payload = {
            "password": password,
            "firstName": first_name
        }
        response = requests.post(
            f'{BASE_URL}{COURIER_CREATE}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_BAD_REQUEST
        assert "message" in response.json()  


    @allure.story("Создание курьера: отсутствует пароль")
    @allure.title("Создание без пароля")
    def test_create_courier_without_password(self, courier_for_validation):
        login = courier_for_validation['login']
        first_name = courier_for_validation['first_name']
        
        payload = {
            "login": login,
            "firstName": first_name
        }
        response = requests.post(
            f'{BASE_URL}{COURIER_CREATE}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_BAD_REQUEST
        assert "message" in response.json()


    @allure.story("Создание курьера: отсутствует имя")
    @allure.title("Создание без имени")
    def test_create_courier_without_first_name(self, courier_for_validation):
        login = courier_for_validation['login']
        password = courier_for_validation['password']
        
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(
            f'{BASE_URL}{COURIER_CREATE}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_CREATED
        assert response.json()["ok"] is True


    @allure.story("Create courier")
    @allure.title("Дубликат логина")
    def test_create_duplicate_courier(self, courier_client, new_courier):
        response = courier_client.create(  
            new_courier['login'],
            new_courier['password'],
            new_courier['first_name']
        )
        assert response.status_code == STATUS_CONFLICT
        assert "message" in response.json()


@allure.story("Create courier")
class TestCourierLogin:


    @allure.story("Login courier")
    @allure.title("Успешный вход")
    def test_login_success(self, courier_client, authorized_courier):
        response = courier_client.login(
            authorized_courier['login'],
            authorized_courier['password']
        )
        assert response.status_code == STATUS_OK
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)  
        

    @allure.story("Login courier")
    @allure.title("Отсутствует логин")
    def test_login_without_login(self):
        courier = Courier()
        courier.generate()
        payload = {"password": courier.password}
        response = requests.post(
            f'{BASE_URL}{COURIER_LOGIN}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_BAD_REQUEST
        assert "message" in response.json()


    @allure.story("Login courier")
    @allure.title("Отсутствует пароль")
    @allure.label('bug', 'true')
    @pytest.mark.xfail(reason="API нестабилен: эндпоинт /login зависает без поля password")
    def test_login_without_password(self, new_courier):
        payload = {"login": new_courier['login']}
        response = requests.post(
            f'{BASE_URL}{COURIER_LOGIN}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_BAD_REQUEST
        assert "message" in response.json()


    @allure.story("Login courier")
    @allure.title("Неверный пароль")
    def test_login_wrong_password(self, new_courier):
        login = new_courier['login']
        wrong_password = "wrong_password_123"
        payload = {"login": login, "password": wrong_password}
        response = requests.post(
            f'{BASE_URL}{COURIER_LOGIN}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        assert response.status_code == STATUS_NOT_FOUND
        assert "message" in response.json()


    @allure.story("Login courier")
    @allure.title("Несуществующий пользователь")
    def test_login_nonexistent_user(self):
        payload = {"login": "Trololo", "password": "123456789qwe" }
        response = requests.post(
            f'{BASE_URL}{COURIER_LOGIN}',
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response_data = response.json()
        assert "message" in response_data
        assert "не найдена" in response_data["message"]


@allure.feature("Courier")
class TestCourierDelete:


    @allure.story("Delete courier")
    @allure.title("Успешное удаление")
    def test_delete_courier_success(self, new_courier, courier_client):
        courier_id = new_courier['id']
        response = courier_client.delete(courier_id)
        assert response.status_code == STATUS_OK
        assert response.json()["ok"] is True
        
    
    @allure.story("Delete courier")
    @allure.title("Удаление без id")
    def test_delete_without_id(self):
        url = f'{BASE_URL}{COURIER_DELETE}'
        response = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)
        assert response.status_code == STATUS_NOT_FOUND
        assert "message" in response.json()


    @allure.story("Delete courier")
    @allure.title("Удаление с несуществующийм id")
    def test_delete_nonexistent_courier(self, courier_client):
        fake_courier_id = 99999999
        response = courier_client.delete(fake_courier_id)
        assert response.status_code == STATUS_NOT_FOUND
        assert "message" in response.json()


    @allure.title("После удаления курьер не может авторизоваться")
    @allure.story("Удаление курьера: Проверка удаления через логин")
    def test_courier_cannot_login_after_delete(self, courier_client, new_courier):
        login = new_courier['login']
        password = new_courier['password']
        courier_id = new_courier['id']
        courier_client.delete(courier_id)
        login_response = courier_client.login(login, password)
        assert login_response.status_code == STATUS_NOT_FOUND
        assert "message" in login_response.json()
