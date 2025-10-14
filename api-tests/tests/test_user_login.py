import pytest
import allure
from data.login_data import LoginTestData

class TestUserLogin:
    
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_existing_user_success(self, api_client, registered_user, validator):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        
        response = api_client.login_user(login_data)
        
        validator.validate_success_response(response, 200)
        assert 'accessToken' in response['data'], "Ответ должен содержать accessToken"
        assert response['data']['user']['email'] == registered_user['email']
    
    @allure.title("Вход с неверным логином и паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("invalid_data", LoginTestData.INVALID_CREDENTIALS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_invalid_credentials_fails(self, api_client, invalid_data, validator):
        response = api_client.login_user(invalid_data)
        
        validator.validate_login_error_response(response)
    
    @allure.title("Вход с пустыми полями")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("empty_data", LoginTestData.EMPTY_FIELDS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_empty_fields_fails(self, api_client, empty_data, validator):
        response = api_client.login_user(empty_data)
        
        validator.validate_login_error_response(response)
    
    @allure.title("Вход без обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_data", LoginTestData.MISSING_REQUIRED_FIELDS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_missing_required_fields_fails(self, api_client, missing_data, validator):
        response = api_client.login_user(missing_data)
        
        validator.validate_login_error_response(response)
    
    @allure.title("Вход с некорректным форматом email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_format_data", LoginTestData.INVALID_FORMATS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_invalid_email_format_fails(self, api_client, invalid_format_data, validator):
        response = api_client.login_user(invalid_format_data)
        
        validator.validate_login_error_response(response)