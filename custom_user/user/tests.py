from django.test import TestCase
from django.db.models import signals
from .models import User, user_post_save

# exceptions
from django.db.utils import IntegrityError
# Create your tests here.


class UserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user('humapen@gmail.com', 'Abc1234567')
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        user = User.objects.create_superuser('humapen@gmail.com', 'Abc1234567')
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_verified)

    def test_users_with_same_emails(self):
        user1 = User.objects.create_user('humapen@gmail.com', 'Abc1234567')
        # creating user with email that already exists should raise an IntegrityError
        self.assertRaises(IntegrityError, User.objects.create_user, 'humapen@gmail.com', 'Abc1234567')

    def test_should_send_signal_on_save(self):
        self.signal_was_called = False

        def handler(sender, **kwargs):
            self.signal_was_called = True

        signals.post_save.connect(handler, sender=User)
        User.objects.create_user('humapen@gmail.com', 'Abc1234567')

        self.assertTrue(self.signal_was_called)
