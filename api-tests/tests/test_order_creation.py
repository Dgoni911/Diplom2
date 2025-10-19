import pytest
import allure
from helpers.api_client import StellarBurgersApiClient
from helpers.response_validator import ResponseValidator
from data.login_data import ErrorMessages


class TestOrderCreation:
    
    @allure.title("Создание заказа с авторизацией")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_order_with_auth_valid_ingredients(self, registered_user, valid_ingredients):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        auth_token = registered_user.get('access_token')
        response = api_client.create_order(valid_ingredients, auth_token)
        
        validator.validate_success_response(response, 200)
        assert 'order' in response.get('data', {}), "Ответ должен содержать информацию о заказе"
        assert response['data']['order'].get('number') is not None, "Заказ должен иметь номер"
    
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_without_auth(self, valid_ingredients):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
    
        response = api_client.create_order(valid_ingredients)
    
        validator.validate_error_response(response, 400, "One or more ids provided are incorrect")
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_empty_ingredients(self, registered_user):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        error_messages = ErrorMessages()
        
        auth_token = registered_user.get('access_token')
        response = api_client.create_order([], auth_token)

        validator.validate_error_response(response, 400, error_messages.INGREDIENTS_REQUIRED)
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_invalid_ingredients_hash(self, registered_user):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        auth_token = registered_user.get('access_token')
        invalid_ingredients = ["invalid_id_1", "invalid_id_2"]
        
        response = api_client.create_order(invalid_ingredients, auth_token)

        validator.validate_error_response(response, 400, "One or more ids provided are incorrect")
    
    @allure.title("Создание заказа с одним ингредиентом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_single_ingredient(self, registered_user, valid_ingredients):
        api_client = StellarBurgersApiClient()
        validator = ResponseValidator()
        
        auth_token = registered_user.get('access_token')
        response = api_client.create_order([valid_ingredients[0]], auth_token)
        
        validator.validate_success_response(response, 200)
        assert 'order' in response.get('data', {}), "Ответ должен содержать информацию о заказе"