import pytest
from app.models import User, AdminGroup
from app import create_app, db
from config import TestConfig
 
@pytest.fixture(scope='module')
def user():
    user = User(id=1,email='patkennedy79@gmail.com',first_name="Jacobia",last_name="Johnson", group_id=1,middle_initial="N")
    user.set_password('unittest')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)
    
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
    # Create the database and the database table
    db.create_all()

    regular_admin_group = AdminGroup(name="Regular", description="This is for all regular administrators.")
    db.session.add(regular_admin_group)

    user = User(id=1,email='patkennedy79@gmail.com',first_name="Jacobia",last_name="Johnson", group_id=regular_admin_group.id,middle_initial="N")
    user.set_password('unittest')
    db.session.add(user)
    
    db.session.commit()

    yield db  # this is where the testing happens!

    db.session.close()
    db.drop_all()
