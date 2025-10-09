import random
import string


class TestData:
    
    @staticmethod
    def generate_unique_user():
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return {
            "email": f"test_user_{random_suffix}@yandex.ru",
            "password": "password123123",
            "name": f"TestUser_{random_suffix}"
        }
    
    def get_existing_user_data(self, registered_user):
        return {
            "email": registered_user['email'],
            "password": registered_user['password'],
            "name": registered_user['name']
        }
    
    def get_user_with_missing_field(self, missing_field):
        user_data = self.generate_unique_user()
        user_data.pop(missing_field)
        return user_data
    
    def get_valid_ingredients(self, api_client):
        try:
            response = api_client.get_ingredients()
            if response.get('success') and 'data' in response:
                ingredients = response['data']
                if ingredients and len(ingredients) >= 2:
                    return [ingredient['_id'] for ingredient in ingredients[:2]]
        except Exception as e:
            print(f"Ошибка при получении ингредиентов: {e}")
        
        return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
    
    @staticmethod
    def get_invalid_ingredients():
        return ["invalid_hash_1", "invalid_hash_2"]
    
    @staticmethod
    def get_empty_ingredients():
        return []
    
    @staticmethod
    def get_invalid_credentials_variants():
        return [
            {"email": "wrong@yandex.ru", "password": "password123123"},
            {"email": "test@yandex.ru", "password": "wrongpassword"},
            {"email": "", "password": "password123123"},
            {"email": "test@yandex.ru", "password": ""}
        ]
    
    @staticmethod
    def get_weak_passwords():
        """Примеры слабых паролей"""
        return ["123", "pass", "a", "short"]