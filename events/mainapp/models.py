from django.db import models
from django.template.defaultfilters import slugify
from transliterate import translit
# Create your models here.


def poster_name(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    link = models.URLField()
    slug = models.SlugField(blank=True)
    venue_name = models.CharField(max_length=150)
    venue_url = models.URLField()
    poster = models.ImageField(upload_to=poster_name)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def month_str(self):
        month_list = ["", "Январь", "Февраль", "Март",
                      "Апрель", "Май", "Июнь",
                      "Июль", "Август", "Сентябрь",
                      "Октябрь", "Ноябрь", "Декабрь"]
        month = self.date.month
        return month_list[month]