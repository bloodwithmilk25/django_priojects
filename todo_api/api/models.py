from django.db import models
from django.urls import reverse


class Todo(models.Model):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("api:todo_detail", kwargs={"pk": self.pk})