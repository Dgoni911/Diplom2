import pytest
import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Регистрация пользователя")
class TestUserRegistration:
    
    @allure.title("Успешная регистрация уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_register_unique_user_success(self, api_client, test_data, validator):
        user_data = test_data.generate_unique_user()
        
        response = api_client.register_user(user_data)
        
        validator.validate_success_response(response, ['accessToken', 'user', 'refreshToken'])
        validator.validate_user_data(response, user_data['email'], user_data['name'])
        validator.validate_response_time(response, max_time=3)
    
    @allure.title("Регистрация уже существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_existing_user_fails(self, api_client, test_data, registered_user, validator):
        existing_user_data = test_data.get_existing_user_data(registered_user)
        
        response = api_client.register_user(existing_user_data)
        
        validator.validate_error_response(
            response, 
            expected_message_keywords=['already exists', 'user exists'],
            expected_status_code=403
        )
    
    @allure.title("Регистрация без обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_missing_field_fails(self, api_client, test_data, validator, missing_field):
        user_data = test_data.get_user_with_missing_field(missing_field)
        
        response = api_client.register_user(user_data)
        
        validator.validate_error_response(
            response,
            expected_message_keywords=['required', 'field'],
            expected_status_code=403
        )
    
    @allure.title("Регистрация с некорректным email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "test@",
        "@domain.com",
        "test@domain",
        ""
    ])
    @pytest.mark.regression
    @pytest.mark.api
    def test_register_user_invalid_email_fails(self, api_client, test_data, validator, invalid_email):
        user_data = test_data.generate_unique_user()
        user_data['email'] = invalid_email
        
        response = api_client.register_user(user_data)
        
        assert response.get('success') == False