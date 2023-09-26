from django.db import models
from django.contrib.auth.models import User
from base.models import base_model
from django.db.models.signals import post_save
from django.dispatch import receiver 
import uuid
from base.email import send_activation_email
from products.models import Product, colorvariant, sizevariant,Coupon





class User_profile(base_model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True,blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False, cart__user = self.user).count()
    
class Cart(base_model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null= True, blank=True)
    is_paid = models.BooleanField(default=False)
    
    def get_cart_total(self):
        cart_items  = self.cart_items.all()
        total = 0
        for cart_item in cart_items:
            total += cart_item.get_product_price()
        
        if self.coupon:
            if self.coupon.minimum_amount < total:
                return total - self.coupon.discount_price
        return total
  

class CartItems(base_model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(colorvariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant  = models.ForeignKey(sizevariant, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_product_price(self):
        price = [self.product.price]
        
        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
            
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)

@receiver(post_save, sender = User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created :
            email_token = str(uuid.uuid4()) 
            User_profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_activation_email(email,email_token)
    except Exception as e:
        print(e)

