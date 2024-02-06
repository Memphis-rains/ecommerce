from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from skimage import measure
import cv2
from zlingoecom.password_util import PasswordUtils
from django.contrib.auth.models import AbstractBaseUser 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# SELLER RELATED STUFF



class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=30)
    business_name = models.CharField(max_length=30,unique=True)
    gstin_number = models.CharField(max_length=100,unique=True)
    seller_shop_address = models.CharField(max_length=100,unique=True)
    seller_email = models.EmailField(max_length=30,unique=True)
    seller_phone = models.CharField(max_length=15,unique=True)
    seller_complaints = models.IntegerField(default=0)
    seller_password=models.CharField(max_length=100)


    def save(self, *args, **kwargs):
        self.seller_password = PasswordUtils.encode_password(self.seller_password)
        super().save(*args, **kwargs)



class Category(models.Model):
    row_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=122, unique=True)

    def clean(self):
        super().clean()

        if self.parent and self.is_descendant_of(self):
            raise ValidationError("Circular reference detected. Category cannot be its own descendant.")

        if self.parent == self:
            raise ValidationError("A category cannot be its own parent.")

        
     
    def is_descendant_of(self, category):
        current_parent = self.parent
        while current_parent:
            if current_parent == category:
                return True
            current_parent = current_parent.parent
        return False

    def save(self, *args, **kwargs):
        self.clean()  

        super().save(*args, **kwargs)

        if self.parent and self.parent != self:
            for child in self.children.all():
                child.save()

                
class Tags(models.Model):
    tag_id=models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name

    



class Variants(models.Model):
    variant_id=models.AutoField(primary_key=True) #1,2
    variant_name = models.CharField(max_length=50)#size=S     
    
    
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_brand = models.CharField(max_length=30)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=122)
    description = models.TextField()
    tags = models.ManyToManyField(Tags, blank=True)
    product_rating = models.PositiveIntegerField(default=0)
    
    

    def get_category_name(self):
        return self.category.name

    def __str__(self):
        return self.product_name
    
    def calculate_ssim(self, image_path1, image_path2):
        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        ssim_index = measure.compare_ssim(gray1, gray2)

        return ssim_index
    
    def save(self, *args, **kwargs):
    
        if self.pk:
            
            existing_products = Product.objects.exclude(pk=self.pk)

            
            for existing_product in existing_products:
                similarity_index = self.calculate_ssim(existing_product.image.path, self.image.path)

                
                if similarity_index >= 0.5:
                    raise ValidationError("Image similarity is too high. Discarding the new image.")

        
        super().save(*args, **kwargs)


class Attribute(models.Model):
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)
    variants = models.ForeignKey(Variants, on_delete=models.CASCADE)
    attr_value = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    variant_image = models.ImageField()

# TOP PICKS AND HOT DEALS
class TopPicks(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)


class ProductReviews(models.Model):
    review_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    review=models.CharField(max_length=200)
    



