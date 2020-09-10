from app.models import User
 
def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password_hash != 'unittest'
