#  Финальный проект Спринт 7: Автотесты API сервиса "Самокат"

## Описание проекта

Проект представляет собой набор автотестов для API учебного сервиса доставки самокатов.  
Тесты покрывают основной функционал: работу с курьерами и заказами.

**URL сервиса:** https://qa-scooter.praktikum-services.ru/  
**Документация API:** https://qa-scooter.praktikum-services.ru/docs/

---

##  Что протестировано

### **Курьеры (Courier)**
| `/api/v1/courier` | POST | Создание курьера |
| `/api/v1/courier/login` | POST | Авторизация курьера |
| `/api/v1/courier/:id` | DELETE | Удаление курьера |

### **Заказы (Orders)**
| `/api/v1/orders` | POST | Создание заказа |
| `/api/v1/orders` | GET | Получение списка заказов |
| `/api/v1/orders/track?t=` | GET | Получение заказа по треку |
| `/api/v1/orders/accept/:id?courierId=` | PUT | Принять заказ |
| `/api/v1/orders/cancel?track=` | PUT | Отменить заказ |


## 📊 Статистика тестов

| Категория | Всего тестов | Passed | XFailed | Failed |
|-----------|--------------|--------|---------|--------|
| Курьеры   | 14           | 13     |       1 |      0 |
| Заказы    | 26           | 18     | 8       | 0      |
| **ИТОГО** | **40**       | **31** | **9**   | **0**  |

---

## 🏗️ Структура проекта
├── api/ # API-клиенты для работы с эндпоинтами
│ ├── init.py
│ ├── courier_client.py # Методы: create(), login(), delete()
│ └── order_client.py # Методы: create(), get_list(), get_by_track(), accept(), cancel()
│
├── models/ # Модели данных
│ ├── init.py
│ ├── courier.py # Класс Courier
│ └── order.py # Класс Order
│
├── tests/ # Тестовые файлы
│ ├── init.py
│ ├── test_courier.py # Тесты на курьеров (14 тестов)
│ └── test_orders.py # Тесты на заказы (26 тестов)
│
├── utils/ # Утилиты и конфигурация
│ ├── init.py
│ ├── api_config.py # Базовый URL, эндпоинты, заголовки
│ ├── api_responses.py # Константы статусов и сообщений
│ └── data_generator.py # Генерация тестовых данных
│
├── conftest.py # Фикстуры pytest (setup/teardown)
├── requirements.txt # Зависимости проекта
├── .gitignore # Исключения для Git
├── allure-report/ # Allure-отчёт (HTML)
└── README.md # Этот файл



Найденные баги API

1
POST /api/v1/courier
Дубликат логина возвращает 409, а не 400 как в документации
✅ Учтено в тестах

2
POST /api/v1/courier/login
Несуществующий пользователь возвращает 404, а не 400
✅ Учтено в тестах

3
POST /api/v1/courier/login
Отсутствует пароль — запрос зависает (таймаут)
⚠️ Помечено как xfail

4
DELETE /api/v1/courier/:id
Несуществующий ID возвращает 404, а не 400
✅ Учтено в тестах

5
POST /api/v1/orders
Обязательные поля не валидируются (создание без полей проходит)
⚠️ Помечено как xfail

6
PUT /api/v1/orders/accept/:id
Отсутствие order_id в URL возвращает 500, а не 400
⚠️ Помечено как xfail



Особенности реализации
Page Object → API Client: Для API использован паттерн API Client (аналог Page Object для UI)
Фикстуры: Все тестовые данные создаются перед тестом и удаляются после (независимость тестов)
Параметризация: Тесты на создание заказа с разными цветами через @pytest.mark.parametrize
Allure-метки: @allure.feature, @allure.story, @allure.title, @allure.label('bug', 'true')
Константы: Все статусы и сообщения об ошибках вынесены в utils/api_responses.py