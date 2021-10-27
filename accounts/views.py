from django.shortcuts import render, redirect, HttpResponseRedirect
from .form import UserCreationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# from classroom.models import ClassRoom
# from classroom.models import Enroll
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


def signuSeller(request):
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
        user.isTeacher = False
        user.isStudent = True
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
        context = {}

        return render(request, 'accounts/buyer/dashboard.html', context)
    return redirect('sellerDashboard')


# @login_required(login_url='signin')
def sellerDashboard(request):
    if request.user.isSeler:
        context = {}
        return render(request, 'accounts/seller/dashboard.html', context)
    return redirect('buyerDashboard')


def signout(request):
    logout(request)
    return redirect('signin')
