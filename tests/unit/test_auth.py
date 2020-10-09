from app.auth.forms import LoginForm


def test_login(test_client):
    form = LoginForm(email="patkennedy79@gmail.com", password="unittest")
    response = test_client.post(
        '/auth/login', data=form.data, follow_redirects=True)

    assert b"Welcome back" in response.data
