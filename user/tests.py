from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from user.models import AuthToken, User

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="andyexample",
            email="andyexample@gmail.com",
            password="admin1",
            first_name="Andy",
            last_name="Cuello"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Token {self.token.key}'

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "andyexample@gmail.com")
        self.assertEqual(self.user.first_name, "Andy")
        self.assertEqual(self.user.last_name, "Cuello")

    def test_user_authentication(self):
        self.assertTrue(self.user.is_authenticated)
        self.assertIsNotNone(self.token)

    def test_user_str_representation(self):
        expected_str = self.user.email 
        self.assertEqual(str(self.user), expected_str)

    def test_user_has_token(self):
        self.assertIsNotNone(self.user.auth_token)
        self.assertEqual(self.user.auth_token, self.token)

    def test_user_can_login(self):
        url = "/api/user/auth"
        data = {
            "username": "andyexample",
            "password": "admin1"
        }
        response = self.client.post(url, data, content_type="application/json")
        self.assertTrue(self.user.check_password(data["password"]))
        self.assertEqual(response.status_code, 200)
