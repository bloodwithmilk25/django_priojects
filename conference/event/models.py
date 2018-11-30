from django.db import models
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from django.urls import reverse
from transliterate import translit
import pyqrcode
# Create your models here.


def image_name(instance,filename):
    # filename consists of transliterated speaker's name
    # if name in latin it stays the same
    filename = translit(instance.first_name, 'ru', reversed=True) + '_' + translit(instance.last_name, 'ru', reversed=True) +'.'+ filename.split('.')[1]
    return "speaker_pics/{}".format(filename)


class Speaker(models.Model):
    first_name = models.CharField(max_length=400)
    last_name = models.CharField(max_length=400)
    position = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)
    photo = models.ImageField(upload_to=image_name, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Confrence(models.Model):
    name = models.CharField(max_length=300)
    discription = models.TextField(max_length=800,blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    speakers = models.ManyToManyField(Speaker)

    def __str__(self):
        return self.name


# method all will return reports ordered by "ordered" field
class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().order_by('-order')


class Report(models.Model):
    title = models.CharField(max_length=300)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False ,blank=True)
    order = models.IntegerField(blank=True)
    objects = ProductManager()

    def __str__(self):
        return self.title


class Visitor(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17) # validators should be a list
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=40)
    country = CountryField()
    verified = models.BooleanField(default=False)
    qrcode = models.ImageField(upload_to=image_name,blank=True)

    def activate(self):
        self.verified = True
        self.save()

    def generate_qr_code(self,request):
        if self.verified:
            # generating qr code
            code = pyqrcode.create(request.build_absolute_uri(), error='M', version=5, mode='binary')
            # trasliterating cyrillic text to latin
            first_name, last_name = (translit(self.first_name, 'ru', reversed=True),
                                     translit(self.last_name, 'ru', reversed=True))
            # path to store qr code
            path_to_qrcode = 'media/visitors_qrcode/{0}_{1}.png'.format(first_name, last_name)
            # saving qr code
            code.png(path_to_qrcode, scale=6, module_color=[0, 0, 0])
            # assinging qr code path to ImageField of Visitor model
            self.qrcode = path_to_qrcode[6:]  # excluding "media/" from path, another way path in admin is media/media/
            self.save()

    def __str__(self):
        return self.first_name + " " + self.last_name+" from: " + self.company

    @staticmethod
    def get_absolute_url():
        return reverse("event:home")


