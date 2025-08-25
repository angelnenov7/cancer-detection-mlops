from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "models/model.joblib"
    DATA_PATH: str = "data/breast_cancer.csv"
    RANDOM_STATE: int = 42
    TEST_SIZE: float = 0.2

    class Config:
        env_file = ".env"

settings = Settings()