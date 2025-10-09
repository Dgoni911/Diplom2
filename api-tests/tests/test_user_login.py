import pytest
import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestUserLogin:
    
    @allure.title("Успешный вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_existing_user_success(self, api_client, registered_user, validator):
        credentials = {
            "email": registered_user['email'],
            "password": registered_user['password']
        }
        
        response = api_client.login_user(credentials)
        
        validator.validate_success_response(response, ['accessToken', 'user', 'refreshToken'])
        validator.validate_user_data(response, registered_user['email'])
        validator.validate_response_time(response, max_time=2)
    
    @allure.title("Вход с неверными учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("invalid_data", [
        {"email": "wrong@yandex.ru", "password": "password123123"},
        {"email": "test@yandex.ru", "password": "wrongpassword"},
        {"email": "", "password": "password123123"},
        {"email": "test@yandex.ru", "password": ""}
    ])
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_invalid_credentials_fails(self, api_client, invalid_data, validator):
        response = api_client.login_user(invalid_data)
        
        validator.validate_error_response(
            response,
            expected_message_keywords=['incorrect', 'invalid', 'unauthorized']
        )
    
    @allure.title("Вход без пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_without_password_fails(self, api_client, test_data, validator):
        credentials = {"email": "test@yandex.ru"}  
        
        response = api_client.login_user(credentials)
        
        validator.validate_error_response(
            response,
            expected_message_keywords=['required', 'field', 'incorrect']
        )
    
    @allure.title("Вход без email")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_without_email_fails(self, api_client, validator):
        credentials = {"password": "password123"}  
        
        response = api_client.login_user(credentials)
        
        validator.validate_error_response(
            response,
            expected_message_keywords=['required', 'field', 'incorrect']
        )