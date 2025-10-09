# Diplom2
Задание 2. Автотесты для API

Косач Евгений 29-я когорта

# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск с генерацией Allure отчета
pytest --alluredir=allure-results

# Просмотр Allure отчета
allure serve allure-results

# Запуск с HTML отчетом
pytest --html=test_reports/report.html


api-tests/
├── .gitignore
├── requirements.txt
├── pytest.ini
├── conftest.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── __init__.py
│   ├── test_data.py
│   └── endpoints.py
├── helpers/
│   ├── __init__.py
│   ├── api_client.py
│   ├── response_validator.py
│   └── wait_utils.py
└── tests/
    ├── __init__.py
    ├── test_user_registration.py
    ├── test_user_login.py
    └── test_order_creation.py

