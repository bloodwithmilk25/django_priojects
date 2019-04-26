from django.db import models


RECIPIENT_CHOICES = (
    ('woman', "Жене"),
    ('girlfriend', "Девушке"),
    ('mom', "Маме"),
    ('dad', "Папе"),
    ('boss', "Начальнику")
)
OCCASION_CHOICES = (
    ('bd', "Дня рождения"),
    ('ny', "Нового года")
)


class Greetings(models.Model):
    recipient = models.CharField(choices=RECIPIENT_CHOICES, max_length=30)
    occasion = models.CharField(choices=OCCASION_CHOICES, max_length=30)
    text = models.TextField()
