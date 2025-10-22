import random
import string

class TestData:
    @staticmethod
    def generate_unique_user():
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return {
            "email": f"test_user_{random_suffix}@yandex.ru",
            "password": "password123",
            "name": f"TestUser_{random_suffix}"
        }
    
    @staticmethod
    def get_existing_user():
        return {
            "email": "existing_user@yandex.ru",
            "password": "password123",
            "name": "ExistingUser"
        }
    
    @staticmethod
    def get_invalid_emails():
        return [
            "invalid-email",
            "test@",
            "@domain.com",
            "test@domain",
            ""
        ]

class OrderTestData:
    @staticmethod
    def get_valid_ingredients():
        """Валидные ингредиенты (примерные ID)"""
        return [
            "643d69a5c3f7b9001cfa093c",  
            "643d69a5c3f7b9001cfa0941",  
            "643d69a5c3f7b9001cfa093e",  
            "643d69a5c3f7b9001cfa0942"   
        ]
    
    @staticmethod
    def get_invalid_ingredients():
        """Невалидные ингредиенты"""
        return [
            "invalid_id_1",
            "invalid_id_2"
        ]