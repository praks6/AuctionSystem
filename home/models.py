from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from accounts.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='productImage')
    category = models.CharField(max_length=100)
    description = models.TextField()
    minimum_price = models.FloatField()
    start_date = models.DateField()
    duration = models.DurationField()
    expire_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class Seller(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User, on_delete=models.SET_NULL,)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user_name


class Bidder(models.Model):
    numeric = RegexValidator(r'^[0-9]', 'Only numerics are allowed.')

    created = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)
    bid_amount = models.CharField(max_length=255, validators=[numeric])

    def __unicode__(self):
        return self.user_name


class Winner(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(User)
    product_id = models.ForeignKey(Product)

    def __unicode__(self):
        return self.user_name
