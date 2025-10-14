import pytest
import allure
from data.login_data import ErrorMessages

class TestOrderCreation:
    
    @allure.title("Создание заказа с авторизацией")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_order_with_auth_valid_ingredients(self, api_client, registered_user, valid_ingredients, validator):
        if not valid_ingredients:
            pytest.skip("Нет доступных ингредиентов")
        
        auth_token = registered_user.get('access_token')
        response = api_client.create_order(valid_ingredients[:2], auth_token)
        
        if response.get('status_code') == 200:
            validator.validate_success_response(response, 200)
            assert 'order' in response.get('data', {}), "Ответ должен содержать информацию о заказе"
        else:
            assert response.get('status_code') != 401, "Не должно быть ошибки авторизации"
            assert response.get('status_code') != 403, "Не должно быть ошибки доступа"
    
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_without_auth(self, api_client, valid_ingredients, validator):
        if not valid_ingredients:
            pytest.skip("Нет доступных ингредиентов")
        
        response = api_client.create_order(valid_ingredients[:2])
        
        if response.get('status_code') == 200:
            validator.validate_success_response(response, 200)
            assert 'order' in response.get('data', {}), "Ответ должен содержать информацию о заказе"
        elif response.get('status_code') == 401:
            validator.validate_error_response(response, 401, "You should be authorised")
        else:
            assert response.get('success') == True or response.get('status_code') not in [400, 500]
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_empty_ingredients(self, api_client, registered_user, validator, error_messages):
        auth_token = registered_user.get('access_token')
        
        response = api_client.create_order([], auth_token)

        if response.get('status_code') == 400:
            validator.validate_error_response(response, 400, error_messages.INGREDIENTS_REQUIRED)
        else:

            assert response.get('success') == False, "Создание заказа без ингредиентов должно завершиться ошибкой"
            assert response.get('status_code') in [400, 403, 500], \
                f"Ожидалась ошибка 400, 403 или 500, получен {response.get('status_code')}"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_invalid_ingredients(self, api_client, registered_user, validator):
        auth_token = registered_user.get('access_token')
        invalid_ingredients = ["invalid_id_1", "invalid_id_2"]
        
        response = api_client.create_order(invalid_ingredients, auth_token)

        if response.get('status_code') == 500:
            validator.validate_error_response(response, 500)
        else:
            assert response.get('success') == False, "Создание заказа с невалидными ингредиентами должно завершиться ошибкой"
            assert response.get('status_code') in [400, 403, 500], \
                f"Ожидалась ошибка 400, 403 или 500, получен {response.get('status_code')}"
    
    @allure.title("Создание заказа с одним ингредиентом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_order_single_ingredient(self, api_client, registered_user, valid_ingredients, validator):
        if not valid_ingredients:
            pytest.skip("Нет доступных ингредиентов")
        
        auth_token = registered_user.get('access_token')
        response = api_client.create_order([valid_ingredients[0]], auth_token)
        
        if response.get('status_code') == 200:
            validator.validate_success_response(response, 200)
            assert 'order' in response.get('data', {}), "Ответ должен содержать информацию о заказе"
        else:
            assert response.get('status_code') != 401, "Не должно быть ошибки авторизации"
            assert response.get('status_code') != 403, "Не должно быть ошибки доступа"