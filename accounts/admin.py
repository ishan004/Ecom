from django.contrib import admin
from .models import User_profile, Cart , CartItems


# Register your models here.
admin.site.register(User_profile)
admin.site.register(Cart)
admin.site.register(CartItems)
