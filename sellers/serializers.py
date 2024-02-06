from rest_framework import serializers
from .models import *
from users.models import *
from users.serializers import *
from django.core.validators import RegexValidator, EmailValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

class SellerSerializer(serializers.ModelSerializer):
    
    gstin_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[A-Z]{1}[0-9A-Z]{1}$'

    
    # gstin_validator = RegexValidator(
    #     regex=gstin_pattern,
    #     message='Enter a valid GSTIN number'
    # )

    email_validator = EmailValidator(
        message='Enter a valid email address'
    )

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Enter a valid phone number'
    )

    class Meta:
        model = Seller
        fields = '__all__'

    
    # def validate_gstin_number(self, value):
    #     self.gstin_validator(value)
    #     return value

    def validate_seller_email(self, value):
        self.email_validator(value)
        return value

    def validate_seller_phone(self, value):
        self.phone_validator(value)
        return value
   
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

    def validate_tag_name(self, value):
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class TopPicksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopPicks
        fields = '__all__'

    def validate_clicked_at(self, value):
        return value

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Attribute
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = '__all__'



class ProductReviewsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = CustomerSerializer(read_only=True)

    class Meta:
        model = ProductReviews
        fields = ['review_id', 'product', 'review', 'user']