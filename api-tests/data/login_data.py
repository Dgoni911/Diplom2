class LoginTestData:
    VALID_CREDENTIALS = {
        "email": "",
        "password": ""
    }
    
    INVALID_CREDENTIALS = [
        {"email": "wrong@yandex.ru", "password": "wrongpassword123"},
        {"email": "nonexistent@example.com", "password": "password123"},
        {"email": "invalid-email", "password": "password123"}
    ]
    
    EMPTY_FIELDS = [
        {"email": "", "password": "password123"},
        {"email": "test@yandex.ru", "password": ""},
        {"email": "", "password": ""}
    ]
    
    INVALID_FORMATS = [
        {"email": "not-an-email", "password": "password123"},
        {"email": "test@", "password": "password123"},
        {"email": "@yandex.ru", "password": "password123"},
        {"email": "test@yandex.", "password": "password123"}
    ]
    
    MISSING_REQUIRED_FIELDS = [
        {"password": "password123"},  
        {"email": "test@yandex.ru"},  
        {}  
    ]


class ErrorMessages:
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    UNAUTHORIZED = "You should be authorised"
    EMAIL_EXISTS = "User with such email already exists"
    INVALID_EMAIL = "email or password are incorrect"  