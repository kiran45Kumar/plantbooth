from django.db import models
from user.models import Customer
from vendor.models import Vendors

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255, blank=True,null=True,default='Another subcategory')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

# New Subcategory Model
class AnotherSubcategory(models.Model):
    name = models.CharField(max_length=255, blank=True,null=True,default='Another subcategory')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='another_subcategories')

    def __str__(self):
        return self.name

# Product model
from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendors, default='', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField(max_length=500)
    product_price = models.CharField(max_length=50)
    category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Subcategory, default="", on_delete=models.CASCADE,blank=True,null=True)
    subsub_category = models.ForeignKey(AnotherSubcategory, default="", on_delete=models.CASCADE,blank=True,null=True)
    product_barcode = models.IntegerField()
    product_quantity = models.IntegerField()
    product_image = models.ImageField(upload_to="products/",default="")
    product_benefits = models.TextField(max_length=1000,default="")  # New field for benefits
    care_tips = models.TextField(max_length=1000,default="")  # New field for care tips
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} -- {self.product_desc}..."

from django.db import models

class DeliveryLocation(models.Model):
    pincode = models.CharField(max_length=6)
    region = models.CharField(max_length=100)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.region} ({self.pincode})"
class Cart(models.Model):
    cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200, default=1)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.product.product_name
class Orders(models.Model):
    CHOICES = [
        ('PENDING','PENDING'),
        ('ORDERED', 'ORDERED'),
        ('SHIPPED', 'SHIPPED'),
        ('DISPATCHED', 'DISPATCHED'),
        ('DELIVERED', 'DELIVERED'),
    ]

    # Order-related fields
    order_id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=200, default="")
    first_name = models.CharField(max_length=100,default='')
    last_name = models.CharField(max_length=100,default='')
    user_phone = models.CharField(max_length=15,default='')
    user_email = models.EmailField(max_length=255,default='')
    user_address = models.TextField(default='')
    user_alternate_phone = models.CharField(max_length=15, blank=True, null=True,default='')
    user_landmark = models.CharField(max_length=255, blank=True, null=True,default='')
    user_city = models.CharField(max_length=100,default='')
    user_state = models.CharField(max_length=100,default='')
    user_country = models.CharField(max_length=100,default='')
    user_postal_code = models.CharField(max_length=10,default='')
    order_notes = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order {self.order_id} by {self.user_name}"