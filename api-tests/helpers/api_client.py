import requests
import allure
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import settings
from data.endpoints import endpoints


class StellarBurgersApiClient:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'StellarBurgers-API-Tests/1.0'
        })
        
        retry_strategy = Retry(
            total=settings.MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
            backoff_factor=settings.RETRY_BACKOFF_FACTOR
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _build_url(self, endpoint):
        return f"{settings.BASE_URL}{endpoint}"
    
    def _get_timeout(self, operation_type="default"):
        return settings.get_timeout(operation_type)
    
    @allure.step("Регистрация пользователя")
    def register_user(self, user_data):
        url = self._build_url(endpoints.REGISTER)
        timeout = self._get_timeout("default")
        response = self.session.post(url, json=user_data, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Авторизация пользователя")
    def login_user(self, credentials):
        url = self._build_url(endpoints.LOGIN)
        timeout = self._get_timeout("quick")
        response = self.session.post(url, json=credentials, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        url = self._build_url(endpoints.ORDERS)
        headers = {}
        if token:
            headers['Authorization'] = token
        
        data = {"ingredients": ingredients}
        timeout = self._get_timeout("slow")
        response = self.session.post(url, json=data, headers=headers, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        url = self._build_url(endpoints.USER)
        headers = {'Authorization': token}
        timeout = self._get_timeout("default")
        response = self.session.delete(url, headers=headers, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Получение данных о пользователе")
    def get_user_info(self, token):
        url = self._build_url(endpoints.USER)
        headers = {'Authorization': token}
        timeout = self._get_timeout("quick")
        response = self.session.get(url, headers=headers, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        url = self._build_url(endpoints.INGREDIENTS)
        timeout = self._get_timeout("quick")
        response = self.session.get(url, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Обновление данных пользователя")
    def update_user_info(self, token, user_data):
        url = self._build_url(endpoints.USER)
        headers = {'Authorization': token}
        timeout = self._get_timeout("default")
        response = self.session.patch(url, json=user_data, headers=headers, timeout=timeout)
        return self._parse_response(response)
    
    @allure.step("Выход из системы")
    def logout_user(self, refresh_token):
        url = self._build_url(endpoints.LOGOUT)
        data = {"token": refresh_token}
        timeout = self._get_timeout("quick")
        response = self.session.post(url, json=data, timeout=timeout)
        return self._parse_response(response)
    
    def _parse_response(self, response):
        try:
            response_data = response.json()
            if isinstance(response_data, dict):
                response_data['status_code'] = response.status_code
                response_data['response_time'] = response.elapsed.total_seconds()
                response_data['headers'] = dict(response.headers)
            return response_data
        except ValueError:
            return {
                "status_code": response.status_code,
                "text": response.text,
                "success": False,
                "response_time": response.elapsed.total_seconds(),
                "headers": dict(response.headers)
            }