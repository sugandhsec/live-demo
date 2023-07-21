import random
from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
def seller_index(request):
    return render(request,"seller_index.html")

def seller_register(request):
    if request.method=="POST":
        try:
            user_data=Seller_User.objects.get(email=request.POST["email"])
            return render(request,"seller_register.html",{"msg":"User Already Exists"})
        except:
            if request.POST["pwd"]==request.POST["cpwd"]:
                global fotp
                fotp=random.randint(100000,999999)
                subject = 'OTP VERIFICATION PROCESS'
                message = f"Thanks For Choosing us Your OTP is {fotp}"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST["email"], ]
                send_mail( subject, message, email_from, recipient_list )
                global temp
                temp={
                    "name":request.POST["name"],
                    "email":request.POST["email"],
                    "password":request.POST["pwd"]
                }
                return render(request,"seller_otp.html")
            else:
                return render(request,"seller_register.html",{"msg":"Password And Confirm Password Not match"})
    else:
        return render(request,"seller_register.html")

def seller_otp(request):
    if request.method=="POST":
        if fotp==int(request.POST["otp"]):
            Seller_User.objects.create(
                    name=temp["name"],
                    email=temp["email"],
                    password=make_password(temp["password"])
                )
            return render(request,"seller_register.html",{"msg":"registration successfull"})
        else:
            return render(request,"seller_otp.html",{"msg":"Otp Not match"})
    else:
        return render(request,"seller_register.html")

def seller_login(request):
    if request.method=="POST":
        try:
            user_data=Seller_User.objects.get(email=request.POST["email"])
            # if user_data.password==request.POST["pwd"]:
            if check_password(request.POST["pwd"],user_data.password):
                request.session["email"]=request.POST["email"]
                session_data=Seller_User.objects.get(email=request.session["email"])
                return render(request,"seller_shop.html",{"session_data":session_data})
            else:
                return render(request,"seller_login.html",{"msg":"Passwrod Not match"})
        except:
            return render(request,"seller_login.html",{"msg":"User Not Exist"})
    else:
        return render(request,"seller_login.html")
    
def seller_logout(request):
    del request.session["email"]
    return render(request,"seller_login.html",{"msg":"Logout Succesfully"})

def seller_profile(request):
    if request.method=="POST":
        session_data=Seller_User.objects.get(email=request.session["email"])
        try:
            image_data=request.FILES["pic"]
        except:
            image_data=session_data.propic
        if request.POST["opwd"] and request.POST["npwd"] and request.POST["cnpwd"]:
            if check_password(request.POST["opwd"],session_data.password):
                if  request.POST["npwd"] == request.POST["cnpwd"]:
                    session_data.name=request.POST["name"]
                    session_data.password=make_password(request.POST["npwd"])
                    session_data.propic=image_data
                    session_data.save()
                else:
                    return render(request,"seller_profile.html",{"session_data":session_data,"msg":"New Passwrod And Confirm New Passwrod Not match"})
            else:
                return render(request,"seller_profile.html",{"session_data":session_data,"msg":"Your Old Password Not match"})
            
        else:
            session_data.name=request.POST["name"]
            session_data.propic=image_data
            session_data.save()
        return render(request,"seller_profile.html",{"session_data":session_data,"msg":"Profile_Updated  Succesfully"})
    else:
        session_data=Seller_User.objects.get(email=request.session["email"])
        return render(request,"seller_profile.html",{"session_data":session_data})
    
    
def add_product(request):
    if request.method=="POST":
        session_data=Seller_User.objects.get(email=request.session["email"])
        Product.objects.create(
            pname=request.POST["pname"],
            price=request.POST["price"],
            pimage =request.FILES["pro_pic"],
            desc  =request.POST["desc"],
            qty =request.POST["qty"],
            seller=session_data
        )
        return render(request,"add_product.html",{"msg":"Product Added Succesfully","session_data":session_data})
    else:
        
        return render(request,"add_product.html",{"session_data":session_data})