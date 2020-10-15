import pytest

from app.models import User


@pytest.mark.usefixtures("user")
class TestUser:
    def test_user(self, user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email, hashed_password, authenticated, and role fields are defined correctly
        """
        assert user.email == 'patkennedy79@gmail.com'
        assert user.password_hash != 'unittest'
        assert user.id == 1
        assert user.first_name == "Pat"
        assert user.last_name == "Kennedy"
        assert user.middle_initial == "N"
        assert user.group_id == 1

    def test_user_retrieval(self, test_client, init_database, user):
        """
        GIVEN a User id
        WHEN a User is retrieved 
        THEN check the user data matches the retrieved User
        """
        assert (user.id == 1)
        retrieved_user = User.query.get(user.id)

        assert (retrieved_user is not None)
        assert (user == retrieved_user)

    def test_user_modification(self, test_client, init_database, user):
        """
        GIVEN a User
        WHEN a User is modified 
        THEN the changes should be reflected in the database
        """

        user.email = 'kennedypat@gmail.com'
        user.set_password('capstoneparking')
        user.first_name = "Kennedy"
        user.last_name = "Pat"
        user.middle_initial = "T"
        user.group_id = 2

        init_database.session.commit()

        updated_user = User.query.get(user.id)

        assert (updated_user == user)
        assert (user.check_password("capstoneparking"))
