from datetime import timezone, datetime

from django.contrib import messages
from django.db.models import Count, Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .form import BidForm, createProduct
from .models import Product, Bidders, Winner


# Create your views here.

def home(request):
    product = Product.objects.all().order_by('-start_date')
    # product = Product.objects.filter(expire_date__lte=datetime.now())
    context = {'product': product}
    return render(request, "home/index.html", context)
def search(request):
    search = request.GET.get('search')
    product = Product.objects.filter(Q(product_name__icontains =search) | Q(description__icontains =search)).order_by('-start_date')
    context = {'product': product}
    return render(request, "home/index.html", context)
################################################################

# @login_required(login_url = 'signin')
def Dashboard(request):
    product = Product.objects.all().order_by('-start_date')
    context = {}
    no_bidder = []
    bid_max_value = []
    winner = []
    for p in product:
        if p.expire_date < datetime.now():
            p.is_expired = True
            p.save()

            bbb = Bidders.objects.filter(product_id=p.id)
            n_bidder = bbb.aggregate(Count('user_id'))['user_id__count']
            no_bidder.append(n_bidder)
            # print(n_bidder)
            if p.is_expired:
                bid_max_val = bbb.aggregate(Max('bid_amount'))['bid_amount__max']
                bid_max_value.append(bid_max_val)
                # print(bid_max_val)

                bidders = Bidders.objects.filter(Q(product_id=p.id) & Q(bid_amount=bid_max_val))
                for b in bidders:
                    winnr = Winner.objects.filter(Q(user_id=b.user_id) & Q(product_id=p.id)).first()
                    winner.append(winnr)
                    if winnr is not None:
                        pass
                    else:
                        Winner.objects.create(product_id=p.id, user_id=b.user_id)

    context = {
               'product': product,
               'bidded_price': bid_max_value,
               'no_bidder': no_bidder,
               'winner': winner,
               }
    return render(request, 'accounts/dashboard.html', context)




######################################################

def productDetails(request, id):
    product = Product.objects.get(pk=id)
    print(id)
    context = {'product': product}

    if request.user.isBuyer:
        form = BidForm(request.POST or None)

        if form.is_valid():
            bid_amount = float(form.cleaned_data['bid_amount'])

            bidder = Bidders.objects.filter(product_id=id, user_id=request.user)
            print(bidder)
            for b in bidder:
                if b is not None:
                    if b.bid_amount == bid_amount and bid_amount <= product.minimum_price:
                        messages.add_message(request, messages.ERROR, "this is ...not valid")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                    b.bid_amount = bid_amount
                    b.save()

                    messages.add_message(request, messages.SUCCESS, "bidded Updated")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


            else:
                bid = form.save(commit=False)
                bid.user = request.user
                bid.product_id = id
                bid.save()
                messages.add_message(request, messages.SUCCESS, "bidded successfully")

        context = {
            'form': form,
            'product': product,
        }

        return render(request, 'accounts/productDetails.html', context)

    return render(request, 'accounts/productDetails.html', context)

#############################################################################

def addProduct(request):
    if request.user.isSeller or request.user.is_admin :
        form = createProduct(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, "product added successfully")
            form = createProduct()
        context = {
            'form': form
        }
        return render(request, 'accounts/seller/create.html', context)
    else:
        return redirect('dashboard')
