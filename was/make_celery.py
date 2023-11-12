from app import create_app
from app.config import CommonConfig

app = create_app(CommonConfig.APP_CONFIG)
celery_app = app.celery_app