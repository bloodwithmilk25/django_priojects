from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models
from transliterate import translit
from django_google_maps import fields as map_fields
import datetime


# helper function to generate image names
def image_name(instance, filename):
    """
    filename consists of transliterated filename and extension
    it is put it the folder with name that corresponds with instance name
    if name was in latin it stays the same
    """
    ext = filename.split('.')[1]
    filename = translit(filename.split('.')[0][:20], 'ru', reversed=True).replace(" ", "") + '.' + ext
    try:
        if instance.path:  # if it's a call from "Image" model
            if instance.location:
                location_name = translit(instance.location.name, 'ru', reversed=True).replace(" ", "")
                return "{}/{}".format(location_name, filename)
            else:
                event_name = translit(instance.event.name, 'ru', reversed=True).replace(" ", "")
                return "{}/{}".format(event_name, filename)
    except AttributeError:
        #  if it's a call from other models, not "Image"
        name = translit(instance.name[:35], 'ru', reversed=True).replace(" ", "")
        return "{}/{}".format(name, filename)


class Category(models.Model):
    name = models.CharField(max_length=35)
    slug = models.SlugField(max_length=35)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=35)
    slug = models.SlugField(max_length=35)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=image_name, blank=True)
    # model "image" is used for the gallery, access it via the 'images' attribute
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = map_fields.AddressField(max_length=200, blank=True)
    geolocation = map_fields.GeoLocationField(max_length=100, help_text="XX.XXX ,YY.YYYY", blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    web_site = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events:location_detail", kwargs={"pk": self.pk})


def year_choices():
    """
    :return: list of tuples of years to choose from, from year 2000 up to current year + 4
    choices takes a tuple of two items The first element in each tuple is the actual value
    to be set on the model, and the second element is the human-readable name.
    """
    return [(r, r) for r in range(2010, datetime.date.today().year+4)]


class EventManager(models.Manager):
    """
    changing get_queryset() to show only published events.
    if all is set to True it will show both published and unpublished
    if False, which is default it will show only published ones
    """
    def get_queryset(self, all=False):
        if not all:
            return super().get_queryset().filter(published=True)
        else:
            return super().get_queryset()


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название события')
    slug = models.SlugField(blank=True, editable=False)
    description = models.TextField(blank=True, verbose_name='Описание')
    short_description = models.TextField(blank=True, verbose_name='Короткое описание')
    web_site = models.URLField(blank=True, verbose_name='Сайт')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='events', null=True, blank=True,
                                 verbose_name='Категория')
    tag = models.ManyToManyField(Tag, related_name='events', blank=True, verbose_name='Тэги')
    year = models.IntegerField(choices=year_choices(), default=datetime.date.today().year, blank=True,
                               verbose_name='Год', help_text='Подтягивается автоматически из даты', editable=False)
    logo = models.ImageField(blank=True, upload_to=image_name, help_text="345x280", verbose_name='Логотип')
    banner = models.ImageField(blank=True, upload_to=image_name, help_text="Ширина 1110px", verbose_name='Баннер')
    date_start = models.DateTimeField(null=True, blank=True, verbose_name='Начало')
    date_end = models.DateTimeField(null=True, blank=True, verbose_name='Конец')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Место проведения')
    parent_event = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                                     verbose_name='Проходит в рамках')
    related_events = models.ManyToManyField('self', blank=True, related_name='related', verbose_name='Связанные события')
    published = models.BooleanField(default=False, verbose_name='Отображать')
    straight_to_site = models.BooleanField(default=False, verbose_name='Перенаправлять сразу на сайт конференции')
    new_tab = models.BooleanField(default=False, verbose_name='Открывать сайт конференции в новой вкладке')
    objects = EventManager()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(translit(self.name, 'ru', reversed=True)[:49])
            if self.date_start:
                self.year = self.date_start.year

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def passed(self):
        """:returns boolean value
        if date_start >= today  >>> False
        else >>> True
        """
        if self.date_start >= datetime.datetime.now(self.date_start.tzinfo):
            return False
        else:
            return True


    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"slug": self.slug})

    def google_calendar_link(self):
        """generates a google calendar link according to event's data and returns it"""
        if self.date_end:
            # checks existence of date_end field,
            # if it's not specified date_end will be equal to date_start
            date_end = self.date_end
        else:
            date_end = self.date_start

        link = "http://www.google.com/calendar/event?action=TEMPLATE" \
               "&dates={year_start}{month_start}{day_start}T080000Z%2F{year_end}{month_end}{day_end}T150000Z" \
               "&text={event_name}" \
               "&location={location}" \
               "&details={description}".format(event_name=self.name, year_start=self.date_start.year,
                                               month_start=self.date_start.strftime('%m'),
                                               day_start=self.date_start.strftime('%d'), year_end=date_end.year,
                                               month_end=date_end.strftime('%m'), day_end=date_end.strftime('%d'),
                                               location=self.location.address, description=self.short_description)
        return link


class Image(models.Model):
    path = models.ImageField(upload_to=image_name)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='images', null=True, blank=True,
                                 help_text="800x530px")
    # image instance can be related to location or event if needed
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    order = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                help_text="Указать если нужно задать свой порядок картинкам")

    def __str__(self):
        return 'Image related to ' + str(self.location) if self.location else str(self.event)
