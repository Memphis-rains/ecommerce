"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard),
    path('products/',views.products),
    path('sellers/',views.sellers),
    path('customers/',views.customers),
    path('sellers/',views.sellers),

    
    path('api-customer/',views.customerGenericApi1.as_view(),name='customer-op'),
    path('api-customer/<int:pk>/',views.customerGenericApi2.as_view(),name='customer-crud'),

    path('api-seller/',views.sellerGenericApi1.as_view(),name='seller-op'),
    path('api-seller/<int:pk>/',views.sellerGenericApi2.as_view(),name='seller-op'),

    path('api-category/',views.categoryGenericApi1.as_view(),name='category-op'),
    path('api-category/<int:pk>/',views.categoryGenericApi2.as_view(),name='category-crud'),
    

    path('api-tag/',views.tagsGenericApi1.as_view(),name='tag-op'),
    path('api-tag/<int:pk>/',views.tagsGenericApi2.as_view(),name='tag-crud'),
    path('add_tags/', views.add_tags, name='add_tags_api'),


    path('api-product/',views.productGenericApi1.as_view(),name='product-op'),
    path('api-product/<int:pk>/',views.productGenericApi2.as_view(),name='product-crud'),


    path('api-variant/',views.variantGenericApi1.as_view(),name='variant-op'),
    path('api-variant/<int:pk>/',views.variantGenericApi2.as_view(),name='variant-crud'),

    path('api-attribute/',views.attributesGenericApi1.as_view(),name='attribute-op'),
    path('api-attribute/<int:pk>/',views.attributesGenericApi2.as_view(),name='attribute-crud')



]