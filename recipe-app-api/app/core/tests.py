from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class CoreTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "blabla@gmail.com"
        password = "password"
        user = get_user_model().object.create_user(email, password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@AtLondonAtdev.com'
        user = get_user_model().object.create_user(email, 'password')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(None, 'password')

    def test_create_new_superuser(self):
        user = get_user_model().object.create_superuser("blabla@gmail.com", 'password')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
