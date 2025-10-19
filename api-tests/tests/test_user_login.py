import pytest
import allure
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.login_data import LoginTestData, ErrorMessages

class TestUserLogin:
    
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_login_existing_user_success(self, registered_user):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
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
    def test_login_invalid_credentials_fails(self, invalid_data):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        response = api_client.login_user(invalid_data)
        
        validator.validate_error_response(response, 401, "email or password are incorrect")
    
    @allure.title("Вход с пустыми полями")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("empty_data", LoginTestData.EMPTY_FIELDS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_empty_fields_fails(self, empty_data):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        response = api_client.login_user(empty_data)
        
        validator.validate_error_response(response, 401, "email or password are incorrect")
    
    @allure.title("Вход без обязательных полей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_data", LoginTestData.MISSING_REQUIRED_FIELDS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_missing_required_fields_fails(self, missing_data):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        response = api_client.login_user(missing_data)
        
        validator.validate_error_response(response, 401, "email or password are incorrect")
    
    @allure.title("Вход с некорректным форматом email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_format_data", LoginTestData.INVALID_FORMATS)
    @pytest.mark.regression
    @pytest.mark.api
    def test_login_invalid_email_format_fails(self, invalid_format_data):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        response = api_client.login_user(invalid_format_data)
        
        validator.validate_error_response(response, 401, "email or password are incorrect")