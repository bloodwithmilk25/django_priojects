from django.db import models

# Create your models here.

class Visitor(models.Model):
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Test(models.Model):
    one = models.CharField(max_length=150)
    two = models.CharField(max_length=150)
    three = models.CharField(max_length=150)
    four = models.CharField(max_length=150)
    five = models.CharField(max_length=150)
    six = models.CharField(max_length=150)
    seven = models.CharField(max_length=150)
    eight = models.CharField(max_length=150)
    nine = models.CharField(max_length=150)

    def __str__(self):
        return self.one


class Test2(models.Model):
    one = models.CharField(max_length=150)
    two = models.CharField(max_length=150)
    three = models.CharField(max_length=150)
    four = models.CharField(max_length=150)
    five = models.CharField(max_length=150)