from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_URL: str
    BASE_AUTH_URL: str
    ADMIN_PASSWORD: str
    ADMIN_LOGIN: str
    SIMPLE_LOGIN: str
    SIMPLE_PASSWORD: str
    FAIL_LOGIN: str
    FAIL_PASSWORD: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')