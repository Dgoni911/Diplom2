import pytest
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.test_data import TestData, OrderTestData
from data.login_data import LoginTestData, ErrorMessages


@pytest.fixture
def valid_ingredients():
    api_client = StellarBurgersApiClient()
    
    try:
        response = api_client.get_ingredients()
        
        if response.get('success') and 'data' in response and isinstance(response['data'], list):
            ingredients = [ingredient['_id'] for ingredient in response['data']]
            if ingredients:
                print(f"Получены актуальные ингредиенты: {len(ingredients)} шт.")
                test_response = api_client.create_order(ingredients[:2])
                if test_response.get('success'):
                    return ingredients[:2]
        
        pytest.skip("Не удалось получить валидные ингредиенты из API")
            
    except Exception as e:
        pytest.skip(f"Ошибка получения ингредиентов: {e}")


@pytest.fixture
def registered_user():
    test_data = TestData()
    api_client = StellarBurgersApiClient()
    
    user_data = test_data.generate_unique_user()
    
    try:
        response = api_client.register_user(user_data)
        
        if response.get('success'):
            access_token = response['data'].get('accessToken', '')
            if access_token.startswith('Bearer '):
                access_token = access_token[7:]  
            
            user_data['access_token'] = access_token
            user_data['refresh_token'] = response['data'].get('refreshToken')
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