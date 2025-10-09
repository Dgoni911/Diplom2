import os


class Settings:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"
    
    CONNECTION_TIMEOUT = 10  
    READ_TIMEOUT = 30        
    
    MAX_RETRIES = 3
    RETRY_BACKOFF_FACTOR = 1  
    
    POLLING_INTERVAL = 2      
    POLLING_TIMEOUT = 60      
    
    TEST_EMAIL_DOMAIN = "yandex.ru"
    DEFAULT_PASSWORD = "password123"
    
    @property
    def IS_DEV(self):
        return "dev" in self.BASE_URL
    
    @property
    def IS_STAGING(self):
        return "staging" in self.BASE_URL
    
    @property
    def IS_PROD(self):
        return "stellarburgers" in self.BASE_URL
    
    def get_timeout(self, operation_type="default"):
        timeouts = {
            "quick": (self.CONNECTION_TIMEOUT, 5),
            "default": (self.CONNECTION_TIMEOUT, self.READ_TIMEOUT),
            "slow": (self.CONNECTION_TIMEOUT, 60),
            "file_upload": (self.CONNECTION_TIMEOUT, 120)
        }
        return timeouts.get(operation_type, timeouts["default"])


settings = Settings()


class EnvironmentSettings:
    
    @property
    def BASE_URL(self):
        return os.getenv("API_BASE_URL", "https://stellarburgers.nomoreparties.site/api")
    
    @property
    def CONNECTION_TIMEOUT(self):
        return int(os.getenv("API_CONNECTION_TIMEOUT", "10"))
    
    @property
    def READ_TIMEOUT(self):
        return int(os.getenv("API_READ_TIMEOUT", "30"))
    
    @property
    def MAX_RETRIES(self):
        return int(os.getenv("API_MAX_RETRIES", "3"))
    
    def get_timeout(self, operation_type="default"):
        base_timeouts = {
            "quick": (self.CONNECTION_TIMEOUT, 5),
            "default": (self.CONNECTION_TIMEOUT, self.READ_TIMEOUT),
            "slow": (self.CONNECTION_TIMEOUT, 60)
        }
        return base_timeouts.get(operation_type, base_timeouts["default"])


