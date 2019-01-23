import logging

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from .tokens import account_activation_token
from celery_learn.celery import app

# https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        instance = UserModel.objects.get(pk=user_id)
        mail_subject = 'Activate your account.'
        message = render_to_string('account_activation_email.html', {
            'user': instance,
            'domain': 'http://localhost:8000',
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)).decode(),
            'token': account_activation_token.make_token(instance),
        })
        instance.email_user(mail_subject, message)
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
