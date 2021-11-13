from datetime import timezone, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Max, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .form import BidForm, createProduct,CommentForm
from .models import Product, Bidders, Winner,Comment,Category

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    product = Product.objects.all().order_by('-start_date')
    # product = Product.objects.filter(expire_date__lte=datetime.now())
    context = {'product': product}
    return render(request, "home/index.html", context)

@login_required(login_url = 'signin')
def search(request):
    search = request.GET.get('search')
    product = Product.objects.filter(Q(product_name__icontains=search) | Q(description__icontains=search)).order_by(
        '-start_date')
    context = {'product': product}
    return render(request, "home/dashboard.html", context)


################################################################

@login_required(login_url = 'signin')
def Dashboard(request):
    category = Category.objects.all()
    product = Product.objects.all().order_by('-start_date')
    paginator = Paginator(product, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'product': page_obj,'category':category}

    return render(request, 'home/dashboard.html', context)


######################################################
@login_required(login_url = 'signin')
def productDetails(request, id):
    product = Product.objects.get(pk=id)
    comments = Comment.objects.filter(product_id=id).order_by('created')

    if product.expire_date < datetime.now():
        product.is_expired = True
        product.save()

    bidder = Bidders.objects.filter(product_id=product.id)
    no_bidder = bidder.aggregate(Count('user_id'))['user_id__count']
    bid_max_val = bidder.aggregate(Max('bid_amount'))['bid_amount__max']

    if product.is_expired:
        winner={}
        bidders = Bidders.objects.filter(Q(product_id=product.id) & Q(bid_amount=bid_max_val))
        for b in bidders:
            winner = Winner.objects.filter(Q(user_id=b.user_id) & Q(product_id=product.id)).first()
            if winner is not None:
                pass

            else:
                Winner.objects.create(product_id=product.id, user_id=b.user_id)

        context = {
            'product': product,
            'comments': comments,
            'bidded_max_price': bid_max_val,
            'no_bidder': no_bidder,
            'winner': winner,
        }

    if request.user.isBuyer and not product.is_expired:
        form = BidForm()
        context = {
            'product': product,
            'comments': comments,
            'bidded_max_price': bid_max_val,
            'no_bidder': no_bidder,
            'form': form,
        }

    if request.user.isSeller or request.user.is_admin:
        context = {
            'product': product,
            'comments': comments,
            'bidded_max_price': bid_max_val,
            'no_bidder': no_bidder,
        }

    return render(request, 'home/productDetails.html', context)


#############################################################################
@login_required(login_url = 'signin')
def afterPaid(request):
    if request.method == 'POST':
        bid_amount = float(request.POST['bid_amount'])
        product_id = request.POST['product_id']
        user = request.POST['user']

        print(type(bid_amount))
        print(product_id)
        print(user)

        product = Product.objects.get(pk=product_id)

        context = {'product': product}

        if Bidders.objects.filter(product_id=product_id, user_id=request.user).exists():
            b= Bidders.objects.get(product_id=product_id, user_id=request.user).bid_amount
            print(b)
            if bid_amount < b and bid_amount <= product.minimum_price:
                messages.add_message(request, messages.ERROR,"Amount can't be less than minimum price and alread "
                                                             "bidded value")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif bid_amount > b:
                bid = get_object_or_404(Bidders, product_id=product_id, user_id=request.user)
                bid.bid_amount =  bid_amount
                bid.save()

                messages.add_message(request, messages.SUCCESS, "updated successfully for given product")

                return render(request, 'home/bidded.html', context)


        else:
            if bid_amount <= product.minimum_price:
                messages.add_message(request, messages.ERROR, "Amount can't be less than minimum price")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            bidder = Bidders.objects.create(user=request.user, product_id=product_id, bid_amount=bid_amount)
            bidder.save()
            messages.add_message(request, messages.SUCCESS, "bidded successfully for given product")

            return render(request, 'home/bidded.html', context)


    messages.add_message(request, messages.ERROR, "Error-you bidded already")
    return render(request, 'home/bidded.html', context)


############################################################################
@login_required(login_url = 'signin')
def addProduct(request):
    if request.user.isSeller or request.user.is_admin:
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


#######################################################

@login_required(login_url = 'signin')
def bid(request, id):
    product = Product.objects.get(pk=id)
    if request.user.isBuyer and not product.is_expired:
        form = BidForm(request.POST or None)

        if form.is_valid():
            request.session['bid_amount'] = request.POST['bid_amount']
            request.session['product'] = Product.objects.get(pk=id).id
            return redirect('payment')

    messages.add_message(request, messages.ERROR, "you can't bid for expired item")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

######################################33

@login_required(login_url = 'signin')
def payment(request):
    bid_amount = request.session.get('bid_amount')
    product_id = request.session.get('product')
    user = request.user
    context_dict = {
        'bid_amount': bid_amount,
        'product_id': product_id,
        'user': user
    }

    if request.method == 'POST':
        a = request.POST['payment_method']
        # print(a)
        if a == 'net_banking':
            return render(request, 'accounts/buyer/net_banking.html', context_dict)
        elif a == 'debit_card':
            return render(request, 'accounts/buyer/debit_card.html', context_dict)
        elif a == 'credit_card':
            return render(request, 'accounts/buyer/credit_card.html', context_dict)

    return render(request, 'accounts/buyer/payment.html', context_dict)

#######################################
@login_required(login_url = 'signin')
def history(request):
    history = Bidders.objects.filter( user_id=request.user)
    context = {'history':history}
    return render(request, 'accounts/buyer/history.html',context)

##########################################
@login_required(login_url = 'signin')
def sellerhistory(request):
    sellerhistory = Product.objects.filter( user_id=request.user)
    context = {'sellerhistory':sellerhistory}
    return render(request, 'accounts/seller/history.html',context)

##########################################
@login_required(login_url = 'signin')
def delete(request, id):
    product = Product.objects.get(pk=id)
    if request.user.isBuyer and not product.is_expired:
        bidderhistory = Bidders.objects.get(product_id=id)
        bidderhistory.delete()

        messages.add_message(request, messages.SUCCESS, "deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.isSeller and not product.is_expired:
        product.delete()

        messages.add_message(request, messages.SUCCESS, "deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    messages.add_message(request, messages.ERROR, "Expired item can not be deleted")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##################################
@login_required(login_url = 'signin')
def get_product_by_category(request):
    cat = request.GET.get("category" or None)
    category = Category.objects.all()

    if cat == "":
        product = Product.objects.all().order_by('-start_date')
        paginator = Paginator(product, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'product': page_obj, 'category': category}

        return render(request, 'home/dashboard.html', context)

    product = Product.objects.filter(category_id=cat)
    paginator = Paginator(product, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'product': page_obj, 'category': category}
    return render(request, 'home/dashboard.html', context)

#################################
@login_required(login_url = 'signin')
def comment(request, id):
    if request.method == 'POST':
        comment =request.POST['comment']

        if Comment.objects.filter(product_id=id, user_id=request.user.id,comment=comment).exists():
            messages.add_message(request, messages.ERROR, "your same comment already exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif comment == "":
            messages.add_message(request, messages.ERROR, "Write something")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            Comment.objects.create(product_id=id, user_id=request.user.id,comment=comment)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url = 'signin')
def editcomment(request, id):
    if request.method == 'POST':
        c = get_object_or_404(Comment, pk=id, user_id=request.user)
        comment = request.POST['comment']
        if comment == "":
            messages.add_message(request, messages.ERROR, "Write something")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            c.comment = comment
            c.save()
        messages.add_message(request, messages.SUCCESS, "comment updated")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    cform =CommentForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'),{'cform':cform})


@login_required(login_url = 'signin')
def deletecomment(request, id):
    c = get_object_or_404(Comment, pk =id, user_id=request.user)
    c.delete()
    messages.add_message(request, messages.ERROR, "comment deleted")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))