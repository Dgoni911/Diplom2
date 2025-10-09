import allure


class ResponseValidator:
    
    @staticmethod
    def validate_success_response(response, expected_fields=None):
        assert response.get('success') == True, f"Expected success=True, got {response}"
        
        if expected_fields:
            for field in expected_fields:
                assert field in response, f"Field '{field}' not found in response: {response}"
        
        allure.attach(str(response), name="Успешный ответ")
    
    @staticmethod
    def validate_error_response(response, expected_message_keywords=None, expected_status_code=None):
        assert response.get('success') == False, f"Expected success=False, got {response}"
        
        if expected_message_keywords:
            message = response.get('message', '').lower()
            found_keywords = []
            for keyword in expected_message_keywords:
                if keyword in message:
                    found_keywords.append(keyword)
            
            assert found_keywords, (
                f"None of expected keywords {expected_message_keywords} "
                f"found in message: {message}"
            )
            
            allure.attach(f"Найдены ключевые слова: {found_keywords}", name="Ключевые слова")
        
        if expected_status_code and 'status_code' in response:
            assert response['status_code'] == expected_status_code, (
                f"Expected status code {expected_status_code}, got {response['status_code']}"
            )
        
        allure.attach(str(response), name="Ответ с ошибкой")
    
    @staticmethod
    def validate_user_data(response, expected_email=None, expected_name=None):
        user_data = response.get('user', {})
        if expected_email:
            assert user_data.get('email') == expected_email, (
                f"Expected email {expected_email}, got {user_data.get('email')}"
            )
        if expected_name:
            assert user_data.get('name') == expected_name, (
                f"Expected name {expected_name}, got {user_data.get('name')}"
            )
    
    @staticmethod
    def validate_order_data(response):
        assert 'name' in response, "Order name not found"
        assert 'order' in response, "Order data not found"
        assert 'number' in response['order'], "Order number not found"
    
    @staticmethod
    def validate_response_time(response, max_time=5):
        if 'response_time' in response:
            response_time = response['response_time']
            assert response_time <= max_time, (
                f"Response time {response_time}s exceeds maximum {max_time}s"
            )
            allure.attach(f"Время ответа: {response_time:.2f}с", name="Производительность")