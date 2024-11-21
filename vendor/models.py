from django.db import models
from user.models import Customer
# Create your models here.
class Vendors(models.Model):
	vendor_id = models.AutoField(primary_key = True)
	user_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
	vendor_name = models.CharField(max_length=200)
	vendor_email = models.CharField(max_length = 50, unique=True)
	vendor_phone = models.CharField(max_length = 50)
	vendor_city = models.CharField(max_length = 50)
	vendor_state = models.CharField(max_length = 50)
	vendor_profile = models.ImageField(upload_to = "uploads/")
	vendor_country = models.CharField(max_length = 50)
	vendor_rating = models.DecimalField(max_digits = 3, decimal_places = 2,default="",blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __str__(self):
		return f"{self.vendor_name} -- {self.vendor_id}"