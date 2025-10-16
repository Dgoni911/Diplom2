import pytest
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.test_data import TestData, OrderTestData
from data.login_data import LoginTestData, ErrorMessages


# Простые фикстуры для объектов
@pytest.fixture
def api_client():
    return StellarBurgersApiClient()


@pytest.fixture
def validator():
    return ResponseValidator()


@pytest.fixture
def test_data():
    return TestData()


@pytest.fixture
def order_test_data():
    return OrderTestData()


@pytest.fixture
def login_test_data():
    return LoginTestData()


@pytest.fixture
def error_messages():
    return ErrorMessages()


@pytest.fixture
def valid_ingredients():
    api_client = StellarBurgersApiClient()
    
    try:
        response = api_client.get_ingredients()
        
        if response.get('success') and 'data' in response and isinstance(response['data'], list):
            ingredients = [ingredient['_id'] for ingredient in response['data']]
            if ingredients:
                return ingredients
        
        return ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa71"]
            
    except Exception:
        return ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa71"]


@pytest.fixture
def registered_user():
    test_data = TestData()
    api_client = StellarBurgersApiClient()
    
    user_data = test_data.generate_unique_user()
    
    try:
        response = api_client.register_user(user_data)
        
        if response.get('success'):
            user_data['access_token'] = response['data'].get('accessToken')
            return user_data
        else:
            pytest.fail(f"Не удалось зарегистрировать пользователя: {response.get('message')}")
            
    except Exception as e:
        pytest.fail(f"Ошибка при регистрации пользователя: {e}")


@pytest.fixture
def unregistered_user():
    test_data = TestData()
    return test_data.generate_unique_user()


@pytest.fixture
def clean_registered_user(registered_user):
    yield registered_user
    
    api_client = StellarBurgersApiClient()
    try:
        api_client.delete_user(registered_user['access_token'])
    except Exception:
        pass  