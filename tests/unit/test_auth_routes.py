from app.auth.forms import LoginForm


class TestAuthRoutes:
    def test_login(self, test_client, init_database):
        form = LoginForm(email="patkennedy79@gmail.com", password="unittest")
        response = test_client.post(
            '/auth/login', data=form.data, follow_redirects=True)

        assert b"Welcome back" in response.data
        assert response.status_code == 200

