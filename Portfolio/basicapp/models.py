from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class Pictures(models.Model):
    name = models.CharField(max_length=150)
    path = models.ImageField(upload_to='photos')
    page = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=60, blank=True)
    email = models.EmailField(max_length=45)
    phone_number = models.CharField(max_length=30, blank=True)
    message = models.CharField(max_length=450)

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return self.first_name + ' ' + self.last_name+ '\n' + self.message


def notify(sender, **kwargs):
    """sends an e-mail notifications when new contact form has been sent"""
    if kwargs["created"]:
        customer = kwargs['instance']
        message = render_to_string('new_contact_notification.html',
                                   {'name': f'{customer.first_name} {customer.last_name}',
                                    'message': customer.message})
        email = EmailMessage('New Contact', message, to=['humapen@gmail.com'])
        email.send()


post_save.connect(notify, sender=Contact)
