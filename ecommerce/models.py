from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from ecommerce.settings import STATUS_SHIPPING, METHODS_PAYMENT, METHODS_NOTIFICATION, COUNTRIES, STATUS_ORDER

# Create your models here.

class UserManager(AbstractUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

# User model.
class User(AbstractUser):
    objects = UserManager()
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email  

# Product model.
class Product(models.Model):
    name = models.CharField('name', max_length=180)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    tax = models.FloatField()
    image = models.CharField('image', max_length=180)
    description = models.TextField()
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

# Order model.
class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    order_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_ORDER, default="")
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

# Shipping model.
class Shipping(models.Model):
    address = models.CharField('address', max_length=250)
    country = models.CharField(max_length=3, choices=COUNTRIES, default="")
    state = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=150, default="")
    zip_code = models.CharField(max_length=10, default="")
    description = models.TextField()
    status = models.CharField(max_length=60, choices=STATUS_SHIPPING, default="")
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

# ProductOrder model.
class ProductOrder(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_id = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    tax = models.FloatField()
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

# Payment model.
class Payment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ManyToManyField(Order)
    paid_value = models.FloatField()
    method_payment = models.CharField(max_length=20, choices=METHODS_PAYMENT, default="")
    approved = models.BooleanField(default=False)
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

# Notification model.
class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField('subject', max_length=200)
    message = models.TextField()
    method_notification = models.CharField(max_length=15, choices=METHODS_NOTIFICATION, default="")
    is_active = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)