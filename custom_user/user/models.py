from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from .managers import UserManager
from .utils import image_name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    avatar = models.ImageField(upload_to=image_name, null=True, blank=True)

    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def short_name(self):
        """
        Returns the short name for the user.
        """
        return f'{self.first_name} {self.last_name[0]}'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

    @staticmethod
    def get_absolute_url():
        return redirect('home')
