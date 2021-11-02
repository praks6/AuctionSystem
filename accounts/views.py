from datetime import datetime

from django.db.models import Max, Q, Count
from django.shortcuts import render, redirect, HttpResponseRedirect

from home.models import Product, Bidders, Winner
from .form import UserCreationForm, LoginForm, createProduct, BidForm
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
        context ={}
        for p in product:
            if p.expire_date < datetime.today().date():
                p.is_expired = True
                p.save()

                bbb = Bidders.objects.filter(product_id=p.id)
                no_bidder = bbb.aggregate(Count('user_id'))['user_id__count']

                if p.is_expired:
                    bid_max_val =bbb.aggregate(Max('bid_amount'))['bid_amount__max']
                    # print(bid_max_val)

                    bidders = Bidders.objects.filter( Q(product_id = p.id) & Q(bid_amount = bid_max_val))
                    print(bidders)
                    for b in bidders:
                        winner = Winner.objects.filter(Q(user_id =b.user_id) & Q( product_id=p.id)).first()
                        if winner is not None:
                            pass
                        else:
                            w=Winner.objects.create(product_id = p.id, user_id =b.user_id)

            # else:
            #     product = Product.objects.filter(is_expired = False)
            #     context = {'product': product}

        context = {'product': product,
                   'bidded_price': bid_max_val,
                   'no_bidder': no_bidder,
                   'winner': winner,
                   }
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
    print(id)
    context = {'product': product}

    if request.user.isBuyer:
        form = BidForm(request.POST or None)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            bidder = Bidders.objects.filter(product_id = id,bid_amount = bid_amount,user_id = request.user)
            # bidder = Bidders.objects.filter(Q(product_id = id) & Q(bid_amount = bid_amount) & Q(user_id = request.user))
            print(bidder.query)
            if bidder is not None:
                messages.add_message(request, messages.ERROR, "bidded already")

            elif bid_amount <= product.minimum_price:
                messages.add_message(request, messages.ERROR, "you can not assign amount less than minimum price")

            else:
                bid = form.save(commit=False)
                bid.user = request.user
                bid.product_id= id
                bid.save()
                messages.add_message(request, messages.SUCCESS, "bidded successfully")

        context = {
            'form': form,
            'product': product
            }

        return render(request, 'accounts/buyer/productDetails.html', context)

    return render(request, 'accounts/buyer/productDetails.html', context)


def addProduct(request):
    if request.user.isSeller:
        form = createProduct(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            product = form.save()
            product.save()
            messages.add_message(request, messages.SUCCESS, "product added successfully")
            form = createProduct()
        context = {
            'form': form
        }
        return render(request, 'accounts/seller/create.html', context)
    else:
        return redirect('buyerDashboard')
