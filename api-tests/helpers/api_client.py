import requests
import allure
from config.urls import URLs
from config.settings import Settings  

class StellarBurgersApiClient:
    def __init__(self):
        self.base_url = URLs.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    @allure.step("Регистрация пользователя")
    def register_user(self, user_data):
        response = self.session.post(
            URLs.REGISTER, 
            json=user_data,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Авторизация пользователя")
    def login_user(self, login_data):
        response = self.session.post(
            URLs.LOGIN, 
            json=login_data,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Удаление пользователя")
    def delete_user(self, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self.session.delete(
            URLs.USER,
            headers=headers,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Получение информации о пользователе")
    def get_user_info(self, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self.session.get(
            URLs.USER,
            headers=headers,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Обновление информации о пользователе")
    def update_user_info(self, user_data, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self.session.patch(
            URLs.USER,
            json=user_data,
            headers=headers,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        response = self.session.get(
            URLs.INGREDIENTS,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients, auth_token=None):
        headers = {}
        if auth_token:
            clean_token = auth_token.replace('Bearer ', '')
            headers["Authorization"] = f"Bearer {clean_token}"
    
        data = {"ingredients": ingredients}
        response = self.session.post(
            URLs.ORDERS, 
            json=data, 
            headers=headers,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = self.session.get(
            URLs.ORDERS,
            headers=headers,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Получение всех заказов")
    def get_all_orders(self):
        response = self.session.get(
            URLs.ORDERS_ALL,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Выход пользователя из системы")
    def logout_user(self, refresh_token):
        data = {"token": refresh_token}
        response = self.session.post(
            URLs.LOGOUT,
            json=data,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    @allure.step("Обновление токена")
    def refresh_token(self, refresh_token):
        data = {"token": refresh_token}
        response = self.session.post(
            URLs.TOKEN,
            json=data,
            timeout=Settings.TIMEOUT
        )
        return self._prepare_response(response)
    
    def _prepare_response(self, response):
        try:
            response_data = response.json()
        except ValueError:
            response_data = {}
        
        return {
            'status_code': response.status_code,
            'success': response_data.get('success', False),
            'message': response_data.get('message', ''),
            'data': response_data,
            'headers': dict(response.headers)
        }