class URLs:
    BASE_URL = "https://stellarburgers.education-services.ru/api"
    
    REGISTER = f"{BASE_URL}/auth/register"
    LOGIN = f"{BASE_URL}/auth/login"
    USER = f"{BASE_URL}/auth/user"
    LOGOUT = f"{BASE_URL}/auth/logout"
    TOKEN = f"{BASE_URL}/auth/token"
    
    ORDERS = f"{BASE_URL}/orders"
    ORDERS_ALL = f"{BASE_URL}/orders/all"
    
    INGREDIENTS = f"{BASE_URL}/ingredients"
    
    PASSWORD_RESET = f"{BASE_URL}/password-reset"
    PASSWORD_RESET_RESET = f"{BASE_URL}/password-reset/reset"