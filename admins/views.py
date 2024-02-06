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
def dashboard(request):
    return render(request,"admin_templates/dashboard.html")

def products(request):
    return render(request,"admin_templates/products.html")

def sellers(request):
    return render(request,"admin_templates/sellers.html")
def customers(request):
    return render(request,"admin_templates/customers.html")

def sellers(request):                                            
    return render(request,"admin_templates/sellers.html")


#SELLER 
class sellerGenericApi1(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['seller_id', 'seller_name', 'seller_name','business_name','seller_email','seller_phone','gstin_number','seller_shop_address']
    search_fields = ['seller_id', 'seller_name','business_name','seller_email','seller_phone','gstin_number','seller_shop_address']
    ordering_fields = ['seller_id', 'seller_name','business_name']
    

class sellerGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset =Seller.objects.all()
    serializer_class = SellerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['seller_id', 'seller_name', 'seller_name','business_name','seller_email','seller_phone']
    search_fields = ['seller_id', 'seller_name','business_name','seller_email','seller_phone']
    ordering_fields = ['seller_id', 'seller_name','business_name']
    pagination_class=PageNumberPagination

#############CUSTOMER END######################

#CUSTOMER 
class customerGenericApi1(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user_name', 'user_email']
    
   


class customerGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset =Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id', 'user_name', 'user_email']
    search_fields = ['user_name', 'user_email']
    ordering_fields = ['user_id', 'user_name']
    pagination_class=PageNumberPagination

#############CUSTOMER END######################


############ CATEGORY ########################## 
class categoryGenericApi1(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields =['parent','name']
    search_fields = ['parent','name']
    ordering_fields = ['parent','name']

    

class categoryGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent','name']
    search_fields =['parent','name']
    ordering_fields = ['parent','name']
    pagination_class=PageNumberPagination

#############CATEGORY END######################

############ Attribute ########################## 
    
class attributesGenericApi1(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    search_fields = ['product__product_id','variants__variant_id','price','attr_value']
    ordering_fields = ['product','variants','price','attr_value']

    def post(self, request, *args, **kwargs):
        image_data = request.data.get('variant_image')

        
        if image_data and isinstance(image_data, str):
            image_data = image_data.split(';base64,')[1]
        
        
        image_data_decoded = base64.b64decode(image_data)
        image_file = ContentFile(image_data_decoded, name="image.jpeg")
        request.data.update({'variant_image': image_file})

        response = super().post(request, *args, **kwargs)

        
        if response.status_code == status.HTTP_201_CREATED:
            product_id = response.data.get('product_id')
            response.data['product_id'] = product_id

        return response


    

class attributesGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    search_fields =['product','variants','price']
    ordering_fields = ['product','variants','price']
    pagination_class=PageNumberPagination

    def post(self, request, *args, **kwargs):
        image_data = request.data.get('variant_image')

        import pdb;pdb.set_trace()
        if image_data and isinstance(image_data, str):
            image_data = image_data.split(';base64,')[1]
        
        
        image_data_decoded = base64.b64decode(image_data)
        image_file = ContentFile(image_data_decoded, name="image.jpeg")
        request.data.update({'variant_image': image_file})

        response = super().post(request, *args, **kwargs)

        
        if response.status_code == status.HTTP_201_CREATED:
            product_id = response.data.get('product_id')
            response.data['product_id'] = product_id

        return response

    
#############CATEGORY END######################


############ TAGS ########################## 


class tagsGenericApi1(generics.ListCreateAPIView):
    queryset =Tags.objects.all()
    serializer_class =TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['tag_id','tag_name']
    ordering_fields = ['tag_id','tag_name']
    pagination_class=LimitOffsetPagination

class tagsGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tag_id','tag_name']
    search_fields =['tag_id','tag_name']
    ordering_fields = ['tag_id','tag_name']
    pagination_class=LimitOffsetPagination


@api_view(['POST'])
def add_tags(request):
    tag_names = request.data.get('tag_name', [])

    tag_ids = []
    for tag_name in tag_names:
        tag_instance, created = Tags.objects.get_or_create(tag_name=tag_name)
        tag_ids.append(tag_instance.tag_id)

    return Response({'tag_ids': tag_ids})
#############CATEGORY END######################



############ PRODUCTS ########################## 

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

import base64
from django.core.files.base import ContentFile

class productGenericApi1(generics.ListCreateAPIView):
    queryset =Product.objects.all()
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    serializer_class =ProductSerializer
    pagination_class=LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    search_fields = ['product_id','product_brand','product_name']
    # ordering_fields = ['product_id','product_brand','product_name','product_brand']

    
   
        
        

class productGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields =['product_id','product_brand','product_name']
    # ordering_fields = ['product_id','product_brand','product_name']

    pagination_class=LimitOffsetPagination

############# PRODUCTS END ######################

############# VARIANTS ######################

class variantGenericApi1(generics.ListCreateAPIView):
    queryset =Variants.objects.all()
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    serializer_class =VariantSerializer
    pagination_class=LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['variant_id','variant_name']
    search_fields =['variant_id','variant_name']
    ordering_fields = ['variant_id','variant_name']


    
        
        

class variantGenericApi2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variants.objects.all()
    serializer_class = VariantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['variant_id','variant_name']
    search_fields =['variant_id','variant_name']
    ordering_fields = ['variant_id','variant_name']
    pagination_class=LimitOffsetPagination

    

############# VARIANT END ######################







