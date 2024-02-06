from django.db import models
from sellers.models import *
from zlingoecom.password_util import PasswordUtils



class Customer(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, db_index=True)
    user_phone = models.CharField(max_length=10, blank=True)
    user_email = models.EmailField(max_length=255, unique=True)
    user_password = models.CharField(max_length=300)
    

    def save(self, *args, **kwargs):
        self.user_password = PasswordUtils.encode_password(self.user_password)
        super().save(*args, **kwargs)
   

class Address(models.Model):
    address_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_name=models.CharField(max_length=100)
    adddress_pincode=models.CharField(max_length=7) 

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    unit_price = models.IntegerField()
    total_price = models.IntegerField()
    order_status=models.CharField(max_length=15,default="PENDING")
    def save(self, *args, **kwargs):
        
        self.unit_price = self.product_id.price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class UserCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        return self.product_id.price * self.quantity
    