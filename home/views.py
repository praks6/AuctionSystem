from datetime import timedelta, datetime

from django.db.models import When
from django.shortcuts import render

from .models import Product


# Create your views here.

def home(request):
    product = Product.objects.all()
    # product = Product.objects.filter(expire_date__lte=datetime.now())
    context = {'product': product}
    return render(request, "home/index.html", context)
