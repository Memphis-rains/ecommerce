
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime,timedelta
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from zlingoecom.password_util import PasswordUtils
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.template.loader import render_to_string
import random
def register(request):
    return render(request,"user_register.html")


def store(request):
    return render(request,"store.html")

def profile(request):
    return render(request,"profile.html")



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
            
            response.set_cookie('touiwertyw5487wtyruiot548y67w54ty858',PasswordUtils.custom_encrypt(user.user_id),secure=True, httponly=True)
            return response

            
        else:
            
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'user_login.html', {'error_message': error_message})

    return render(request, 'user_login.html')

class CustomerAPIView(generics.ListCreateAPIView):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user_name', 'user_email']

    def get_queryset(self):
        
        encrypted_user_id = self.request.COOKIES.get('touiwertyw5487wtyruiot548y67w54ty858','')

        print(encrypted_user_id)
        if encrypted_user_id:
            
            queryset = Customer.objects.filter(user_id=PasswordUtils.custom_decrypt(encrypted_user_id))
            print(queryset)
            return queryset

        
        return queryset


    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   

   
class CustomerAPIView2(generics.RetrieveUpdateDestroyAPIView):
    queryset =Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_id', 'user_name', 'user_email']
    search_fields = ['user_name', 'user_email']
    ordering_fields = ['user_id', 'user_name']
    pagination_class=PageNumberPagination
    
    def get(self, request, *args, **kwargs):
        encrypted_user_id = request.COOKIES.get('touiwertyw5487wtyruiot548y67w54ty858', '')
        
        
        if encrypted_user_id:
            try:
                user = Customer.objects.get(user_id=PasswordUtils.custom_decrypt(encrypted_user_id))
                serializer = self.serializer_class(user)
                return Response(serializer.data)

            except (Customer.DoesNotExist, ValueError):
                
                return Response({'detail': 'User not found or invalid user_id'}, status=404)

        
        return redirect('/users')



def reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if Customer.objects.filter(user_email=email).exists():
            random_number = ''.join(str(random.randint(0, 9)) for _ in range(7))
            subject = "Verfication Alert"
            message = render_to_string('verificationalert.html',{'code':random_number})
            from_email = "lms.cait@google.com"
            recipient_list = [email]
            send_mail(
                subject,
                '',
                from_email,
                recipient_list,
                html_message=message
            )
            response = redirect("confirmcode")
            response.set_cookie('confirm_code', random_number, secure=True, httponly=True)
            response.set_cookie('profemail', email, secure=True, httponly=True)
            return response
        else:
            invalid_email = True
            return render(request, "forgot_password.html",{'invalid_email': invalid_email})
    return render(request, "forgot_password.html")

def confirm_code(request):
    con_code = request.COOKIES.get('confirm_code')
    if request.method == 'POST':
        code = request.POST.get('code')
        if con_code and int(con_code) == int(code):
            print("VALID CODE")
            response = redirect('reset_code')
            response.delete_cookie('confirm_code')
            return response
        else:
            invalid_code=True
            return render(request, "ConfirmCode.html",{'invalid_code': invalid_code})
    return render(request, "ConfirmCode.html")

def reset_code(request):
    prof_email = request.COOKIES.get('profemail')
    current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')    
    
    if not prof_email :
        return redirect("/")

    if request.method == "POST":
        response = redirect("http://127.0.0.1:8000/users/")
        code1 = request.POST.get('code1')
        code2 = request.POST.get('code2')

        if code1 == code2:
            professor = Customer.objects.get(user_email=prof_email)
            professor.user_password = code1
            professor.save()
            subject = "Password Change Confirmation"
            message = render_to_string('codcgd.html',{'cd':code2,'dt':current_date_time})
            from_email = "lms.cait@google.com"
            recipient_list = [prof_email]
            send_mail(
                subject,
                '',
                from_email,
                recipient_list,
                html_message=message
                )
            response.delete_cookie('profemail')
            return  response
            
        else:
            
            return render(request, 'resetCode.html', {'codes_do_not_match': True})

    return render(request, 'resetCode.html')
    