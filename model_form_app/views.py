from django.contrib.auth import models
from django.contrib.messages.api import success
from django.shortcuts import render ,redirect
from django.http.response import HttpResponse
from django.views.generic.edit import UpdateView
from .models import EmpPersonal
from .forms import EmpPersonalModelForm,EmpPersonalForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.views import View
from django.views.generic import CreateView,ListView
import random

import django.urls 




# Create your views here.
def user_model_form(request):
    form = EmpPersonalModelForm()
    print(form)
    if request.method == 'POST':
        save_form = EmpPersonalModelForm(request.POST)
        if save_form.is_valid():
            save_form.save()
            return HttpResponse('Registered successfully!')
        else:
            return HttpResponse('Invalid data')
    return render(request,"model_form.html",{'form':form})

def user_form(request):
    form = EmpPersonalForm()
    if request.method == 'POST':
        name      = request.POST.get('name')
        mobile    = request.POST.get('mobile')
        per_mail  = request.POST.get('per_mail')
        age       = request.POST.get('age')
        address   = request.POST.get('address')
        county    = request.POST.get('county')
        print(name,mobile,per_mail,age,address,county)
        #emp_info = EmpPersonal(name=name,mobile=mobile,per_mail=per_mail,age=age,address=address,county=county)
        #emp_info.save()
        EmpPersonal.objects.create(name=name,mobile=mobile,per_mail=per_mail,age=age,address=address,county=county)
    return render(request,'form.html',{'form':form})

def user_html_form(request):
    if request.method == 'POST':
        name      = request.POST.get('name')
        password  = request.POST.get('password')
        mobile    = request.POST.get('mobile')
        per_email  = request.POST.get('per_email')
        age       = request.POST.get('age')
        address   = request.POST.get('address')
        country    = request.POST.get('country')
        photo =request.FILES.get('photo')
        #print(name,mobile,per_mail,age,address,county)
        user_data = User.objects.create(username=name,email=per_email,is_active=True,is_staff=True)
        user_data.set_password(password) 
        user_data.save()
        EmpPersonal.objects.create(name=name,mobile=mobile,per_email=per_email,age=age,address=address,country=country,user=user_data)  
    return render(request,'html_form.html')

def get_user_list(request):
        all_data = {}
        if request.user.is_authenticated:
                if request.user.is_superuser:
                      all_data = EmpPersonal.objects.all()
                else:
                      all_data = EmpPersonal.objects.filter(user=request.user)
        return render(request,'all_data.html',{'data':all_data})

def get_single_data(request,id):
    get_data = EmpPersonal.objects.get(id=id)
    return render(request,'single_data.html',{'data':get_data})

def update_data(request,id):
    get_data = EmpPersonal.objects.get(id=id)
    if request.method == 'POST':
        name       = request.POST.get('name')
        mobile     = request.POST.get('mobile')
        per_email  = request.POST.get('per_email')
        age        = request.POST.get('age')
        address    = request.POST.get('address')
        country    = request.POST.get('country')
        filter_data = EmpPersonal.objects.filter(id=id)
        filter_data.update(name=name,mobile=mobile,per_email=per_email,age=age,address=address,country=country)    
        return HttpResponse('Updated Successfull!!!!')
    return render(request,'update_form.html',{'data':get_data})

def delete_user(request,id):
    EmpPersonal.objects.get(id=id).delete()
    return HttpResponse('User deleted Successfully!!!')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        check_user = authenticate(username=username,password=password)
        if check_user:
                login(request,check_user)
                messages.success(request,"Hi {} , you are Logged in successfully".format(check_user))
                return redirect('get_user_list')

        else:
                messages.warning(request,'Invalid Credentials , Try Again!')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    messages.success(request,'Logout Successfully!')
    return redirect('user_login')

def user_send_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        email_check = User.objects.filter(email=email)
        if email_check:
            otp_save      =  EmpPersonal.objects.filter(per_email=email)
            print(otp_save[0]) # purna
            otp           =  random.randint(100000,999999) 
            save_data     =  otp_save[0]
            save_data.otp =  str(otp) 
            save_data.save()  #save in the DB
            msg='Hi {},\n You have requested for a forgot password verification{}'.format(email_check[0].username,otp)
            send_mail('Password change Verification',msg,settings.EMAIL_HOST_USER,[email_check[0].email])
            return redirect('verify_otp')
        else:
               messages.warning(request,'Email id is incorrect')
    return render(request,'send_email.html')

def verify_otp(request):
    if request.method == 'POST':
        gen_otp = request.POST['otp']
        check_otp = EmpPersonal.objects.filter(otp=gen_otp)
        if check_otp:
               return redirect('new_password',id=check_otp[0].id)
        else:
            messages.warning(request,'Please Enter correct OTP')
    return render(request,'verify_otp.html')

def new_password(request,id):
    emp_info = EmpPersonal.objects.get(id=id)
    print(emp_info)
    if request.method == 'POST':
            password = request.POST['password']
            check_mail = emp_info.per_email    
            user_data  = User.objects.get(email=check_mail)
            user_data.set_password(password)
            user_data.save()
            return redirect('user_login')
    return render(request,'new_password.html')

class EmpPersonal_cls(CreateView):
    models =EmpPersonal
    field='__all__'

class EmpPersonal_List(ListView):
    model =EmpPersonal

class EmpPersonal_Update(UpdateView):
    model=EmpPersonal
    fields=('name','mobile','per_email','age','address','country')  