import os
from dotenv import load_dotenv

load_dotenv()


class CommonConfig:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    APP_CONFIG = os.environ.get("APP_CONFIG")
    SWAGGER_UI_DOC_EXPANSION="full"
    SWAGGER_UI_REQUEST_DURATION = True


class LocalConfig(CommonConfig):
    APP_CONFIG = "local"
    DEBUG = True
    TESTING = False
    REDIS_URL = "redis://localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    CACHE_TYPE = "simple"
    CACHE_REDIS_URL = REDIS_URL


class TestConfig(CommonConfig):
    APP_CONFIG = "test"
    DEBUG = True
    TESTING = True
    REDIS_URL = None
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    CACHE_TYPE = "simple"


class DevelopmentConfig(CommonConfig):
    APP_CONFIG = "dev"
    DEBUG = True
    TESTING = False
    REDIS_URL = "redis://redis:6379/0"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATA_URI", None)

    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = REDIS_URL


class ProductionConfig(CommonConfig):
    APP_CONFIG = "prod"
    DEBUG = False
    TESTING = False
    REDIS_URL = os.environ.get("REDIS_URL")

    SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_DATA_URI", None)
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = REDIS_URL


config_dic = {
    "local": LocalConfig,
    "test": TestConfig,
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}
