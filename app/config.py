from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "PocketSmart AI"
    SECRET_KEY: str = "dev-secret-change-me"
    SESSION_SECRET: str = "dev-session-secret-change-me"
    JWT_SECRET: str = "dev-jwt-secret-change-me"
    DATABASE_URL: str = "sqlite:///./pocketsmart.db"

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"
    AI_ENABLED: bool = True

    MAX_UPLOAD_MB: int = 5
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_image_types(self) -> set[str]:
        return {x.strip() for x in self.ALLOWED_IMAGE_TYPES.split(",") if x.strip()}

settings = Settings()
