# Базовый URL API
BASE_URL = 'https://qa-scooter.praktikum-services.ru'

# Эндпоинты для работы с курьерами
COURIER_CREATE = '/api/v1/courier'
COURIER_LOGIN = '/api/v1/courier/login'
COURIER_DELETE = '/api/v1/courier'  # + /:id в URL

# Эндпоинты для работы с заказами
ORDER_CREATE = '/api/v1/orders'
ORDER_LIST = '/api/v1/orders'
ORDER_BY_TRACK = '/api/v1/orders/track'
ORDER_ACCEPT = '/api/v1/orders/accept'  # + /:id?courierId=:id
ORDER_CANCEL = '/api/v1/orders/cancel'  # ?track=:track
ORDER_FINISH = '/api/v1/orders/finish'  # + /:id

# Заголовки по умолчанию
HEADERS = {'Content-Type': 'application/json'}

# Таймаут для запросов (в секундах)
TIMEOUT = 60