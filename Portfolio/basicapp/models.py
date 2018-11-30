from django.db import models
from django.urls import reverse


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
