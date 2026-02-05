from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- DATABASE SETTINGS ---
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "test_db"
    COLLECTION: str = "employees"

    # --- SERVER SETTINGS ---
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    PROJECT_NAME: str = "Employee API"


settings = Settings()
