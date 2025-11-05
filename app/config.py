from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Document Summarizer API"
    version: str = "1.0.0"
    max_content_length: int = 50000  # 50KB max input
    rate_limit_requests: int = 10
    rate_limit_window: int = 60  # seconds
    summary_ratio: float = 0.3  # 30% of original length

settings = Settings()
