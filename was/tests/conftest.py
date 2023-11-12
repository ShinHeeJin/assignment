from typing import Generator

import pytest
from app import create_app, db
from flask import Flask
from pytest import FixtureRequest


@pytest.fixture(scope="module")
def app(request: type[FixtureRequest]) -> Flask:
    app = create_app("test")
    assert app.testing is True
    context = app.app_context()
    context.push()

    def teardown():
        db.drop_all()
        context.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def api_client(app: Flask) -> Generator:
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def headers():
    return {"Content-Type" : "application/json"}