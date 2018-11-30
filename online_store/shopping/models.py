from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return "{}".format(self.username)

    def get_absolute_url(self):
        return reverse("shop:home")


class Category(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category", kwargs={"slug": self.slug})

def pre_save_category_slug(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_category_slug, sender=Category)
#-------------------------------------------------------------------------

class Brand(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name
#-------------------------------------------------------------------------

# переопределяем базовый менеджер модели, чтобы изметить метод all
# class ProductManager(models.Manager):
#     def all(self, *args, **kwargs):
#         return super(ProductManager, self).get_queryset().filter(avaliable=True)

# making goodlooking image names
def image_name(instance,filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products') # related_name - name of the context ketword when using Category model
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_name)
    price = models.PositiveIntegerField()
    avaliable = models.BooleanField(default=True)
    #objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
                                                "slug": self.slug,
                                                "category": self.category.slug,})

# -------------------------------------------------------------------------------------


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)

    def __str__(self):
        return str(self.product)

    def change_item_quantity(self, qnt):
        self.quantity = int(qnt)
        self.item_price = self.quantity * Decimal(self.product.price)
        self.save()


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    total = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)

    def __str__(self):
        return str(self.id)


    def add_to_cart(self,product):
        new_item = CartItem.objects.get_or_create(product=product, item_price = product.price)[0]
        if new_item not in self.items.all():
            self.items.add(new_item)
            self.save()


    def remove_from_cart(self,product):
        try:
            item = self.items.get(product__title=product.title)
            self.items.remove(item)
        except:
            None

    def total_amount(self):
        total = 0.0
        for item in self.items.all():
            total += item.product.price * item.quantity
        self.total = total
        self.save()
        return self.total


#-------------------------------------------------------------------------
User = get_user_model()
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('performing', 'Perfoming'),
    ('completed', 'Completed'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    items = models.ManyToManyField(Cart)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    shipping_adress = models.CharField(max_length=250,blank=True)
    shipping_type = models.CharField(max_length=40, choices=(('pickup','Pickup'), ('shipping','Shipping')),default='shipping')
    status = models.CharField(max_length=40, choices=ORDER_STATUS_CHOICES)
    cost = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    comments = models.TextField(blank=True)

    def __str__(self):
        return 'Order №{}'.format(str(self.id))

    def get_absolute_url(self):
        return reverse("shop:thankyou",kwargs={'id':self.id})

    def get_order_products_info(self):
        '''
        returns a list of list of [product, quantity, total price]
        --> [iPhone, 2, 2000]
        --> [iMac, 1, 5000]
        '''
        products = []
        for cart in self.items.all():
            for cart_item in cart.items.all():
                info = []
                info.append(cart_item.product)
                info.append(cart_item.quantity)
                info.append(cart_item.item_price)
                products.append(info)
        return products
