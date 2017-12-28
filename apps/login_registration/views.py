from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages
from django.contrib.messages import error

# render routes
def index(request):
    return render(request,"login_registration/index.html")

def logout(request):
    request.session.clear()
    return redirect(reverse('lr:index'))

# post routes
def register(request):
    if request.method == "POST":        
        result = User.objects.validate(request.POST)
        if type(result) == User:
        # we can also do if type(result) == list, but we consider the best ones first
            request.session['user_id'] = result.id
            messages.success(request, 'Successfully registered!!!')
            return redirect(reverse('lr:success'))
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
            return redirect(reverse('lr:success'))
        else:
            for err in result:
                messages.error(request, err)       
    return redirect(reverse('lr:index'))
        
def success(request):
    try:
        me = User.objects.get(id=request.session['user_id'])
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request,"login_registration/success.html", context)
    except:
        return redirect(reverse('lr:index'))
