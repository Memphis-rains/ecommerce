from django.contrib.auth.models import User
from django.db import models
import bcrypt
from zlingoecom.password_util import PasswordUtils

class AdminProfile(models.Model):
   
    admin_id=models.AutoField(primary_key=True) 
    admin_name = models.CharField(max_length=255)
    admin_email = models.EmailField()
    amin_phone_number = models.CharField(max_length=10) 
    amdin_password=models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
    
        self.user_password = PasswordUtils.encode_password(self.user_password)
        super().save(*args, **kwargs)

