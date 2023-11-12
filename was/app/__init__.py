from .config import config_dic
from celery import Celery, Task
from datetime import datetime
from flask import Flask, Blueprint, g
from flask import g
from flask_caching import Cache
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
import uuid

db = SQLAlchemy()
cache = Cache()
celery_app = Celery()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config["APP_CONFIG"] = config_name
    app.config.from_object(config_dic[config_name])

    configure_extensions(app)
    configure_json_encoder(app)
    configure_errorhandlers(app)
    initialize_database(app)
    init_before_app_request(app)

    return app


def init_before_app_request(app):
    @app.before_request
    def before_request():
        # global request uuid
        g.req_uuid = uuid.uuid4().hex


def initialize_database(app):
    with app.app_context():
        db.create_all()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    app.config.from_mapping(
        CELERY=dict(
            broker_url=app.config["REDIS_URL"],
            result_backend=app.config["REDIS_URL"],
            task_ignore_result=True,
        )
    )
    app.config.from_prefixed_env()

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.celery_app = celery_app
    return celery_app


def configure_extensions(app: Flask) -> None:
    from app.controllers.post_controller import ns as post_namespace

    blueprint = Blueprint("app", __name__)
    api = Api(
        blueprint,
        title="Post API",
        description="Post CRUD API Document",
        doc="/docs",
        validate=False,
        version="0.1.0",
    )
    api.add_namespace(post_namespace, path="/post")
    app.register_blueprint(blueprint, url_prefix="/api")
    app.restx_api = api

    # db
    db.init_app(app)

    # celery
    celery_init_app(app)

    # cache
    cache.init_app(app)
    with app.app_context():
        cache.clear()


def configure_errorhandlers(app: Flask) -> None:
    from werkzeug.exceptions import HTTPException
    from marshmallow.exceptions import ValidationError

    @app.errorhandler(HTTPException)
    def default_http_errorhandler(error):
        db.session.rollback()
        db.session.close()
        if hasattr(error, "description"):
            message = error.description
            status_code = error.code
        elif isinstance(error, ValidationError):
            message = str(error.args[0]) if error.args else ""
            status_code = HTTPStatus.BAD_REQUEST
        else:
            message = str(error.args[0]) if error.args else ""
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        req_uuid = getattr(g, "req_uuid", None)
        return {"data": {}, "result": {"msg": message, "req_uuid": req_uuid}}, status_code

    app.restx_api.handle_error = default_http_errorhandler


def configure_json_encoder(app):
    from flask.json.provider import DefaultJSONProvider

    class CustomJSONEncoder(DefaultJSONProvider):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            return super().default(obj)

    app.json = CustomJSONEncoder(app)
