from app.models import User


def test_user(user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password_hash != 'unittest'
    assert user.id == 1
    assert user.first_name == "Jacobia"
    assert user.last_name == "Johnson"
    assert user.middle_initial == "N"
    assert user.group_id == 1
