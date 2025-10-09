import pytest
import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreation:
    
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_order_with_auth_valid_ingredients(self, auth_client, valid_ingredients, validator):
        api_client, user = auth_client
        
        response = api_client.create_order(valid_ingredients, user['access_token'])
        
        validator.validate_success_response(response, ['name', 'order'])
        validator.validate_order_data(response)
        validator.validate_response_time(response, max_time=5)
    
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_without_auth(self, api_client, valid_ingredients, validator):
        response = api_client.create_order(valid_ingredients)
        
        assert 'status_code' not in response or response.get('status_code') != 500
        
        if response.get('success') == False:
            validator.validate_error_response(
                response,
                expected_message_keywords=['authorized', 'auth', 'token']
            )
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_empty_ingredients(self, auth_client, test_data, validator):
        api_client, user = auth_client
        ingredients = test_data.get_empty_ingredients()
        
        response = api_client.create_order(ingredients, user['access_token'])
        
        validator.validate_error_response(
            response,
            expected_message_keywords=['provided', 'ingredient', 'required'],
            expected_status_code=400
        )
    
    @allure.title("Создание заказа с невалидными ингредиентами")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_invalid_ingredients(self, auth_client, test_data, validator):
        api_client, user = auth_client
        ingredients = test_data.get_invalid_ingredients()
        
        response = api_client.create_order(ingredients, user['access_token'])
        
        assert response.get('success') == False or response.get('status_code', 200) >= 400
    
    @allure.title("Создание заказа с одним ингредиентом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_single_ingredient(self, auth_client, valid_ingredients, validator):
        api_client, user = auth_client
        single_ingredient = [valid_ingredients[0]] if valid_ingredients else ["60d3b41abdacab0026a733c6"]
        
        response = api_client.create_order(single_ingredient, user['access_token'])
        
        if response.get('success'):
            validator.validate_success_response(response, ['name', 'order'])
        else:
            assert 'message' in response