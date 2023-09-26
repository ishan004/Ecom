from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import User_profile
from products.models import *
from accounts.models import  Cart , CartItems




def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username= email)
        
        if not user_obj.exists():
            messages.warning(request, "Account does not exist")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Account is not verified")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')
        
        messages.warning(request, "Invalid username or password")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')
        
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        
        if user_obj.exists():
            messages.warning(request, "Email already registered")
            return HttpResponseRedirect(request.path_info)
        
        print(email)
        
        user_obj = User.objects.create(first_name = first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request, "An email has been sent to your mail.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def activate_email(request,email_token):
    try:
        user= User_profile.objects.get(email_token = email_token)
        user.is_email_verified= True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid email token")

def add_to_cart(request , uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid= uid )
    user = request.user 
    cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    cart_items = CartItems.objects.create(cart = cart, product=product  )
    
    if variant:
        variant = request.GET.get('variant')
        size_variant = sizevariant.objects.get(size_name = variant )
        cart_items.size_variant = size_variant
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    


   
def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    cart_total = cart.get_cart_total()
    
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request, "Invalid Coupon code")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.coupon:
            messages.warning(request, "Coupon already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request, f'Coupon is expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, cart.coupon.coupon_code +" Coupon applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'cart': cart, 'cart_total': cart_total} 
    return render(request, 'accounts/cart.html', context )  
        
def remove_coupon(request , cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

