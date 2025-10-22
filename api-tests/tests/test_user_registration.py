import pytest
import allure
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.test_data import TestData
from data.login_data import ErrorMessages

class TestUserRegistration:
    
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_register_unique_user_success(self):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        test_data = TestData()
        
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
    def test_register_existing_user_fails(self):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        test_data = TestData()
        error_messages = ErrorMessages()
        
        user_data = test_data.generate_unique_user()
        api_client.register_user(user_data)
        
        response = api_client.register_user(user_data)
        
        validator.validate_error_response(response, 403, error_messages.USER_EXISTS)
    
    @allure.title("Создание пользователя без обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_missing_field_fails(self, missing_field):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        test_data = TestData()
        error_messages = ErrorMessages()
        
        user_data = test_data.generate_unique_user()
        user_data.pop(missing_field)  
        
        response = api_client.register_user(user_data)
        
        validator.validate_error_response(response, 403, error_messages.REQUIRED_FIELDS)
    
    @allure.title("Регистрация с некорректным email форматом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "test@",
        "@domain.com",
        "no-at.com",
        "spaces in@email.com"
    ])
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_invalid_email_format_fails(self, invalid_email):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        test_data = TestData()
        
        user_data = test_data.generate_unique_user()
        user_data['email'] = invalid_email
        
        response = api_client.register_user(user_data)
        
        assert response.get('success') == False, f"Регистрация с email '{invalid_email}' должна завершиться ошибкой"
        
        expected_statuses = [400, 403, 500]
        assert response.get('status_code') in expected_statuses, \
            f"Ожидался один из статусов {expected_statuses}, получен {response.get('status_code')}"
    
    @allure.title("Регистрация с пустым email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_empty_email_fails(self):
        api_client = StellarBurgersApiClient()
        test_data = TestData()
        
        user_data = test_data.generate_unique_user()
        user_data['email'] = ""
        
        response = api_client.register_user(user_data)
        
        assert response.get('success') == False, "Регистрация с пустым email должна завершиться ошибкой"
        assert "required" in response.get('message', '').lower(), \
            "Для пустого email должно быть сообщение о обязательных полях"
