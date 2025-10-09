import time
import allure
from typing import Callable, Optional
from config.settings import settings


class WaitUtils:
    
    @staticmethod
    @allure.step("Ожидание выполнения условия")
    def wait_for_condition(
        condition: Callable[[], bool],
        timeout: Optional[int] = None,
        interval: Optional[int] = None,
        description: str = "Условие выполнено"
    ) -> bool:
        
        timeout = timeout or settings.POLLING_TIMEOUT
        interval = interval or settings.POLLING_INTERVAL
        end_time = time.time() + timeout
        
        with allure.step(f"Ожидание: {description} (таймаут: {timeout}с)"):
            attempt = 1
            while time.time() < end_time:
                if condition():
                    elapsed = time.time() - (end_time - timeout)
                    allure.attach(
                        f"Условие выполнено на попытке {attempt} через {elapsed:.1f}с",
                        name="Время ожидания"
                    )
                    return True
                
                time.sleep(interval)
                attempt += 1
            
            allure.attach(f"Таймаут ожидания превышен после {attempt} попыток", 
                         name="Результат ожидания")
            return False
    
    @staticmethod
    @allure.step("Ожидание успешного ответа API")
    def wait_for_successful_response(api_call: Callable, expected_status: int = 200, **kwargs):
        
        def check_response():
            try:
                response = api_call(**kwargs)
                if hasattr(response, 'status_code'):
                    return response.status_code == expected_status
                elif isinstance(response, dict) and 'status_code' in response:
                    return response['status_code'] == expected_status
                return False
            except Exception:
                return False
        
        return WaitUtils.wait_for_condition(
            check_response,
            description=f"Успешный ответ API (статус {expected_status})"
        )
    
    @staticmethod
    @allure.step("Ожидание появления данных")
    def wait_for_data(api_call: Callable, data_validator: Callable, **kwargs):
        
        def check_data():
            try:
                response = api_call(**kwargs)
                return data_validator(response)
            except Exception:
                return False
        
        return WaitUtils.wait_for_condition(
            check_data,
            description="Появление ожидаемых данных в ответе"
        )
    
    @staticmethod
    def wait_for_order_creation(api_client, token, expected_order_count=1):
        
        def check_order_created():
            try:
                return True
            except Exception:
                return False
        
        return WaitUtils.wait_for_condition(
            check_order_created,
            description=f"Создание заказа (ожидается: {expected_order_count})"
        )