import pytest
import allure
import requests
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.test_data import TestData


@pytest.fixture(scope="session")
def api_client():
    return StellarBurgersApiClient()


@pytest.fixture(scope="session")
def test_data():
    return TestData()


@pytest.fixture(scope="session")
def validator():
    return ResponseValidator()


@pytest.fixture
def registered_user(api_client, test_data):
    user_data = test_data.generate_unique_user()
    access_token = None
    
    try:
        response = api_client.register_user(user_data)
        if response.get('success'):
            access_token = response.get('accessToken', '')
            user_data['access_token'] = access_token
            user_data['refresh_token'] = response.get('refreshToken', '')
        else:
            user_data['access_token'] = None
            user_data['refresh_token'] = None
    except Exception as e:
        user_data['access_token'] = None
        user_data['refresh_token'] = None
    
    yield user_data
    
    if access_token:
        try:
            api_client.delete_user(access_token)
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")


@pytest.fixture
def auth_client(api_client, registered_user):
    return api_client, registered_user


@pytest.fixture
def valid_ingredients(api_client, test_data):
    return test_data.get_valid_ingredients(api_client)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        pass


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: Smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
    config.addinivalue_line(
        "markers", "api: API tests"
    )