from django.db import models

# Create your models here.
class Customer(models.Model):
    role_choices = [
    ('admin','Admin'),
    ('customer','Customer'),
    ('vendor','Vendor'),
]
    user_id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 50,default='')
    user_email = models.CharField(max_length = 50,unique=True)
    user_password = models.CharField(max_length = 50, default='')
    user_phone = models.IntegerField()
    role = models.CharField(max_length = 50, choices = role_choices,default='customer')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
	    return f"{self.user_name} -- {self.user_email}"

