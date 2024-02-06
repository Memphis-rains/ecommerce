from users.models import *
from django.core.validators import RegexValidator, validate_email
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    
        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_quantity(self, value):
        return value

    def validate_order_status(self, value):
        return value

class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'

    def validate_quantity(self, value):
        return value

    def validate(self, data):
        return data    