from django.test import TestCase
from django.db.models import signals
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import reverse

from .models import User, user_post_save
from .tokens import account_activation_token

# exceptions
from django.db.utils import IntegrityError


class UserTest(TestCase):
    def create_user(self):
        return User.objects.create_user('humapen@gmail.com', 'Abc1234567')

    def test_create_user(self):
        user = self.create_user()
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        user = User.objects.create_superuser('humapen@gmail.com', 'Abc1234567')
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_verified)

    def test_users_with_same_emails(self):
        self.create_user()
        # creating user with email that already exists should raise an IntegrityError
        self.assertRaises(IntegrityError, User.objects.create_user, 'humapen@gmail.com', 'Abc1234567')

    def test_should_send_signal_on_save(self):
        self.signal_was_called = False

        def handler(sender, **kwargs):
            self.signal_was_called = True

        signals.post_save.connect(handler, sender=User)
        self.create_user()

        self.assertTrue(self.signal_was_called)

    def test_new_user_verification(self):
        new_user = self.create_user()
        # visit activation link
        link = reverse('verify',
                       kwargs={'uidb64': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                               'token': account_activation_token.make_token(new_user)})
        resp = self.client.get(link)
        new_user.refresh_from_db()

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(new_user.is_verified)

    def test_confirm_view(self):
        self.create_user()
        self.client.login(username='humapen@gmail.com', password='Abc1234567')
        resp = self.client.get(reverse('confirm'))

        self.assertContains(resp, 'Confirm')

    def test_redirect_annonymous_user_from_confirm(self):
        resp = self.client.get(reverse('confirm'))

        self.assertRedirects(resp, reverse('profile'))

    def test_redirect_verified_user_from_confirm(self):
        user = self.create_user()
        user.is_verified = True
        self.client.login(username='humapen@gmail.com', password='Abc1234567')
        resp = self.client.get(reverse('confirm'))

        self.assertRedirects(resp, reverse('profile'))
