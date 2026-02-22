from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PORT: int = 8000
    GRPC_PORT: int = 50051

    # MinIO / S3
    AWS_ACCESS_KEY_ID: str = "minioadmin"
    AWS_SECRET_ACCESS_KEY: str = "minioadmin"
    AWS_ENDPOINT_URL: str = "http://minio-service:9000"
    S3_BUCKET_NAME: str = "dvc-storage"

    # ClearML
    CLEARML_WEB_HOST: str = "http://clearml-web:8080"
    CLEARML_API_HOST: str = "http://clearml-api:8008"
    CLEARML_FILES_HOST: str = "http://clearml-files:8081"
    CLEARML_API_ACCESS_KEY: str = ""
    CLEARML_API_SECRET_KEY: str = ""

    DATA_DIR: str = "/app/data"

    class Config:
        env_file = ".env"


settings = Settings()