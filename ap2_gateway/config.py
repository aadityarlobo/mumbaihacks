from pydantic_settings import BaseSettings

class AP2Config(BaseSettings):
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "healthcare_surge"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    
    # Gateway Settings
    GATEWAY_PORT: int = 8002
    MAX_CONCURRENT_PAYMENTS: int = 10
    PROCESSING_TIME_MIN_SECONDS: int = 1
    PROCESSING_TIME_MAX_SECONDS: int = 5
    SUCCESS_RATE: float = 0.95
    
    # Security
    HMAC_SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Idempotency
    IDEMPOTENCY_WINDOW_HOURS: int = 24
    
    # Retry Logic
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_SECONDS: int = 10
    
    # Webhooks
    WEBHOOK_TIMEOUT_SECONDS: int = 30
    WEBHOOK_MAX_RETRIES: int = 5
    
    class Config:
        env_file = ".env"

config = AP2Config()
