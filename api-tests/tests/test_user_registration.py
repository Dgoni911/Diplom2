import pytest
import allure
from data.test_data import TestData
from data.login_data import ErrorMessages

class TestUserRegistration:
    
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_register_unique_user_success(self, api_client, test_data, validator):
        user_data = test_data.generate_unique_user()
        
        response = api_client.register_user(user_data)
        
        validator.validate_success_response(response, 200)
        assert 'accessToken' in response['data'], "Ответ должен содержать accessToken"
        assert response['data']['user']['email'] == user_data['email']
        assert response['data']['user']['name'] == user_data['name']
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_existing_user_fails(self, api_client, test_data, validator, error_messages):
        user_data = test_data.generate_unique_user()
        api_client.register_user(user_data)
        
        response = api_client.register_user(user_data)
        
        validator.validate_error_response(response, 403, error_messages.USER_EXISTS)
    
    @allure.title("Создание пользователя без обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_missing_field_fails(self, api_client, test_data, validator, error_messages, missing_field):
        user_data = test_data.generate_unique_user()
        user_data.pop(missing_field)  
        
        response = api_client.register_user(user_data)
        
        validator.validate_error_response(response, 403, error_messages.REQUIRED_FIELDS)
    
    @allure.title("Регистрация с некорректным email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_email", TestData.get_invalid_emails())
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_invalid_email_fails(self, api_client, test_data, validator, invalid_email):
        user_data = test_data.generate_unique_user()
        user_data['email'] = invalid_email
        
        response = api_client.register_user(user_data)
        
        assert response.get('success') == False, "Регистрация с некорректным email должна завершиться ошибкой"
        assert response.get('status_code') in [400, 403, 500], \
            f"Ожидалась ошибка 400, 403 или 500, получен {response.get('status_code')}"