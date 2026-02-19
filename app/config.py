import os


def _development_database_uri() -> str:
    return (
        os.getenv("DATABASE_URL")
        or os.getenv("DEV_DATABASE_URL")
        or "sqlite:///instance/dev.db"
    )


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _development_database_uri()


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
