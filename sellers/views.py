from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from sellers.models import *
from rest_framework.decorators import api_view
from sellers.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Q
from users.models import * 
from django.db import transaction
from rest_framework.pagination import LimitOffsetPagination
from zlingoecom.password_util import PasswordUtils
from django.shortcuts import render, redirect

def seller_home(request):
    return render(request,"seller_templates/seller_home.html")


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Customer.objects.get(user_email=email)
        except Customer.DoesNotExist:

            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'user_login.html', {'error_message': error_message})


        if PasswordUtils.check_password(user.user_password, password):

            response = redirect("/users")
            
            response.set_cookie('N@#*65n^@#%8^N35N(*^35@#%^*)',PasswordUtils.custom_encrypt(user.user_id),secure=True, httponly=True)
            return response

            
        else:
            
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'user_login.html', {'error_message': error_message})

    return render(request, 'user_login.html')


class sellerGenericApi1(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['seller_id', 'seller_name', 'seller_name','business_name','seller_email','seller_phone','gstin_number','seller_shop_address']
    search_fields = ['seller_id', 'seller_name','business_name','seller_email','seller_phone','gstin_number','seller_shop_address']
    ordering_fields = ['seller_id', 'seller_name','business_name']
  