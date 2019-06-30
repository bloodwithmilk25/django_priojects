from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField()

    def __str__(self):
        return f'{self.name} {self.pk}'


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=250)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    year = models.IntegerField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
