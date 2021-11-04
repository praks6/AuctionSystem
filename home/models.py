from datetime import datetime, timezone, timedelta

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from accounts.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/productimage/")
    category = models.CharField(max_length=100)
    description = models.TextField()
    minimum_price = models.FloatField()
    start_date = models.DateTimeField()
    duration = models.IntegerField()
    expire_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_expired = models.BooleanField(blank=True, null= True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.expire_date = self.start_date + timedelta(days=self.duration)
        super(Product, self).save(*args, **kwargs)


    @property
    def remaining_time(self):
        return self.expire_date-datetime.now()


class Bidders(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_amount = models.FloatField()


class Winner(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user_name
