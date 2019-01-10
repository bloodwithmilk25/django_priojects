from django.db import models
from django.urls import reverse


class Cell(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    taken = models.BooleanField(default=False)
    occupied_by = models.CharField(blank=True, max_length=100)

    class Meta:
        unique_together = ('row', 'column')
        ordering = ['pk']

    def __str__(self):
        return f'ROW{self.row}, COL{self.column}'

    def get_absolute_url(self):
        return reverse("api:cell", kwargs={"pk": self.pk})