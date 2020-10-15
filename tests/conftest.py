import os

import pytest

from app import create_app, db
from app.models import User, AdminGroup
from config import TestingConfig


@pytest.fixture
def user():
    user = User(id=1, email='patkennedy79@gmail.com', first_name="Pat", last_name="Kennedy", group_id=1,
                middle_initial="N")
    user.set_password('unittest')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestingConfig)
    is_travis = 'TRAVIS' in os.environ
    if is_travis:
        flask_app.config[
            'SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:@127.0.0.1:3306/flask_capstone_schema"

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.drop_all()
    # Create the database and the database table
    db.create_all()

    regular_admin_group = AdminGroup(name="Regular", description="This is for all regular administrators.")
    db.session.add(regular_admin_group)

    user = User(id=1, email='patkennedy79@gmail.com', first_name="Pat", last_name="Kennedy",
                group_id=regular_admin_group.id, middle_initial="N")
    user.set_password('unittest')
    db.session.add(user)

    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.close()
    db.drop_all()
