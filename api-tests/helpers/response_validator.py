class ResponseValidator:
    
    def validate_success_response(self, response, expected_status_code=200):
        assert response.get('status_code') == expected_status_code, \
            f"Ожидался статус код {expected_status_code}, получен {response.get('status_code')}"
        assert response.get('success') == True, "Ответ должен быть успешным"
    
    def validate_error_response(self, response, expected_status_code, expected_message=None):
        assert response.get('status_code') == expected_status_code, \
            f"Ожидался статус код {expected_status_code}, получен {response.get('status_code')}"
        assert response.get('success') == False, "Ответ должен быть неуспешным"
        
        if expected_message:
            actual_message = response.get('message', '')
            assert expected_message.lower() in actual_message.lower(), \
                f"Ожидалось сообщение '{expected_message}', получено '{actual_message}'"
    
    def validate_login_error_response(self, response):
        self.validate_error_response(response, 401, "email or password are incorrect")