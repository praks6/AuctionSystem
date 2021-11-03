from django.shortcuts import render, redirect
from .form import UserCreationForm, LoginForm
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
            return redirect('dashboard')
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


def signout(request):
    logout(request)
    return redirect('signin')
