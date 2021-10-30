from django.shortcuts import render, redirect, HttpResponseRedirect

from home.models import Product
from .form import UserCreationForm, LoginForm, createProduct, Bid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def signin(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.isSeller:
                return redirect('sellerDashboard')
            elif user.isBuyer:
                return redirect('buyerDashboard')
            logout(request)
            messages.add_message(request, messages.ERROR, "login with either seller or buyer")
            return redirect('signin')
        messages.add_message(request, messages.ERROR, "email and password does not match")
    return render(request, 'accounts/login.html', context={'form': form})


def signupSeller(request):
    form = UserCreationForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        user = form.save()
        user.isSeller = True
        user.isBuyer = False
        user.set_password(request.POST['password'])
        user.save()
        messages.add_message(request, messages.SUCCESS, "signup successfully")
        return redirect('signin')
    context = {
        'form': form
    }
    return render(request, 'accounts/seller/signup.html', context)


def signupBuyer(request):
    form = UserCreationForm(request.POST or None)
    print(request.POST)
    if form.is_valid():
        user = form.save()
        user.isSeller = False
        user.isBuyer = True
        user.set_password(request.POST['password'])
        user.save()
        messages.add_message(request, messages.SUCCESS, "signup successfully")
        return redirect('signin')
    context = {
        'form': form
    }
    return render(request, 'accounts/buyer/signup.html', context)


# @login_required(login_url='signin')
def buyerDashboard(request):
    if request.user.isBuyer:
        product = Product.objects.all()
        context = {'product': product}
        return render(request, 'accounts/buyer/dashboard.html', context)
    return redirect('sellerDashboard')


# @login_required(login_url='signin')
def sellerDashboard(request):
    if request.user.isSeller:
        product = Product.objects.all()
        context = {'product': product}
        return render(request, 'accounts/seller/dashboard.html', context)
    return redirect('buyerDashboard')


def signout(request):
    logout(request)
    return redirect('signin')


######################################################
def productDetails(request, id):
    product = Product.objects.filter(pk=id)
    context = {'product': product, }
    if request.user.isBuyer:
        form = Bid(request.POST or None, )
        if form.is_valid():
            bid = form.save()
            bid.product_id= request.POST['pid']
            bid.user_id = request.user
            bid.save()
        return render(request, 'accounts/buyer/productDetails.html', context,{'form':form})


    return render(request, 'accounts/buyer/productDetails.html', context)


def addProduct(request):
    if request.user.isSeller:
        form = createProduct(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            product = form.save()
            # product.user_id = request.user
            product.save()
            messages.add_message(request, messages.SUCCESS, "product added successfully")
            form = createProduct()
        context = {
            'form': form
        }
        return render(request, 'accounts/seller/create.html', context)
    else:
        return redirect('buyerDashboard')
