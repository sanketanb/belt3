from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages
from django.contrib.messages import error

# render routes
def index(request):
    return render(request,"login_registration/index.html")

def create_display(request):
    return render(request,"login_registration/create_display.html")

def logout(request):
    request.session.clear()
    messages.success(request, 'Successfully logged out!!!')
    return redirect(reverse('lr:index'))

def product_display(request, product_id):
    this_product = Product.objects.get(id=product_id)
    product_data = {
        'product': this_product,
        'wishes': this_product.wishes.all()
    }
    return render(request,"login_registration/product_display.html", product_data)

# logic routes
def register(request):
    if request.method == "POST":        
        result = User.objects.validate(request.POST)
        if type(result) == User:
        # we can also do if type(result) == list, but we consider the best ones first
            request.session['user_id'] = result.id
            messages.success(request, 'Successfully registered!!!')
            return redirect(reverse('lr:dash'))
        else:
            for err in result:
                messages.error(request, err)            
    return redirect(reverse('lr:index'))

def login(request):
    if request.method == "POST":
        result = User.objects.validate_login(request.POST)
        if type(result) == User:            
            request.session['user_id'] = result.id
            messages.success(request, 'Successfully logged in!!!')
            return redirect(reverse('lr:dash'))
        else:
            for err in result:
                messages.error(request, err)       
    return redirect(reverse('lr:index'))
        
def dash(request):
    try:
        me = User.objects.get(id=request.session['user_id'])
        wishes = User.objects.get(id=request.session['user_id']).wishes.all()
        excluded_products_id=[wish.product.id for wish in wishes]

        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'wishes': wishes,
            'products': Product.objects.all().exclude(id__in=excluded_products_id)
        }
        return render(request,"login_registration/dash.html", context)
    except:
        return redirect(reverse('lr:index'))

def add_new_product(request):
    if request.method == "POST":
        id=request.session['user_id']
        result = Product.objects.validate_new_product(request.POST, id)
        if type(result) == Product:   
            me = User.objects.get(id=request.session['user_id'])
            Wish.objects.create(product=result, user=me)         
            messages.success(request, 'Successfully added the product-',result.product_name)
            return redirect(reverse('lr:dash'))
        else:
            for err in result:
                messages.error(request, err)  
    return redirect(reverse('lr:create_display'))

def add_to_wish(request, id):
    this_product = Product.objects.get(id=id)
    me = User.objects.get(id=request.session['user_id'])
    Wish.objects.create(product=this_product, user=me)
    return redirect(reverse('lr:dash'))

def remove_from_wish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.delete()
    return redirect(reverse('lr:dash'))

def delete(request, product_id):
    this_product = Product.objects.get(id=product_id)
    this_product.delete()
    return redirect(reverse('lr:dash'))