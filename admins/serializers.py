from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, validate_email
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class AdminProfileSerializer(serializers.ModelSerializer):
    
    admin_name = serializers.CharField(max_length=255, validators=[
        RegexValidator(
            regex='^[A-Za-z\s]+$',
            message='Only letters and spaces are allowed.',
            code='invalid_admin_name'
        )
    ])

    admin_email = serializers.EmailField(validators=[validate_email])

    admin_phone_number = serializers.CharField(max_length=10, validators=[
        RegexValidator(
            regex='^\d{10}$',
            message='Phone number must be a 10-digit number.',
            code='invalid_phone_number'
        )
    ])

    class Meta:
        model = AdminProfile
        fields = '__all__'
