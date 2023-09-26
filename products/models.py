from django.db import models
from base.models import base_model
from django.utils.text import slugify

class category(base_model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null= True, blank= True)
    category_image = models.ImageField(upload_to ="categories")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(category, self).save(*args, **kwargs)
    
    def __str__ (self) -> str:
        return self.category_name

class colorvariant(base_model):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__ (self) -> str:
        return self.color_name

class sizevariant(base_model):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    
    def __str__ (self) -> str:
        return self.size_name
    
class Product(base_model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank = True)
    category = models.ForeignKey(category, on_delete = models.CASCADE, related_name = "products")
    price = models.IntegerField()
    product_descp = models.TextField()
    color_variant = models.ManyToManyField(colorvariant, blank= True)
    size_variant = models.ManyToManyField(sizevariant, blank= True)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.product_name
    
    
    def get_product_price_by_size(self, size):
        return self.price + sizevariant.objects.get(size_name = size).price
    

    

class ProductImage(base_model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name = "product_images")
    image = models.ImageField(upload_to = "product")
    

class Coupon(base_model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
                                 