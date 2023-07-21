import random
from django.shortcuts import render,redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
from app_seller.models import *
from django.db.models import Q
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            return render(request,"register.html",{"msg":"User Already Exists"})
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
                return render(request,"otp.html")
            else:
                return render(request,"register.html",{"msg":"Password And Confirm Password Not match"})
    else:
        return render(request,"register.html")
    
def otp(request):
    if request.method=="POST":
        if request.POST["otp"]:
            if fotp==int(request.POST["otp"]):
                User.objects.create(
                        name=temp["name"],
                        email=temp["email"],
                        password=make_password(temp["password"])
                    )
                return render(request,"register.html",{"msg":"registration successfull"})
            else:
                return render(request,"otp.html",{"msg":"Otp Not match"})
        else:
            return render(request,"otp.html",{"msg":"Please Enter Otp"})
    else:
        return render(request,"register.html")
    
def login(request):
    if request.method=="POST":
        try:
            user_data=User.objects.get(email=request.POST["email"])
            # if user_data.password==request.POST["pwd"]:
            if check_password(request.POST["pwd"],user_data.password):
                request.session["email"]=request.POST["email"]
                session_data=User.objects.get(email=request.session["email"])
                return render(request,"shop.html",{"session_data":session_data})
            else:
                return render(request,"login.html",{"msg":"Passwrod Not match"})
        except:
            return render(request,"login.html",{"msg":"User Not Exist"})
    else:
        return render(request,"login.html")
    
# def login_msg(request,mymsg):
#     return render(request,"login.html",{"msg":mymsg})
    
def logout(request):
    try:
        request.session["email"]
        del request.session["email"]
        return render(request,"login.html",{"msg":"Logout Succesfully"})
    except:
        return render(request,"login.html",{"msg":"Cannot Logout Without Login"})
    # return redirect('login',msg="Logout Succesfully")

def profile(request):
    if request.method=="POST":
        session_data=User.objects.get(email=request.session["email"])
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
                    return render(request,"profile.html",{"session_data":session_data,"msg":"New Passwrod And Confirm New Passwrod Not match"})
            else:
                return render(request,"profile.html",{"session_data":session_data,"msg":"Your Old Password Not match"})
            
        else:
            session_data.name=request.POST["name"]
            session_data.propic=image_data
            session_data.save()
        return render(request,"profile.html",{"session_data":session_data,"msg":"Profile_Updated  Succesfully"})
    else:
        session_data=User.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"session_data":session_data})
    
    
def shop(request):
    session_data=User.objects.get(email=request.session["email"])
    all_product=Product.objects.all()
    return render(request,"shop.html",{"all_product":all_product,"session_data":session_data})

def single_product(request,pk):
    session_data=User.objects.get(email=request.session["email"])
    one_data=Product.objects.get(id=pk)
    return render(request,"single-product.html",{"one_data":one_data,"session_data":session_data})

def add_to_cart(request,pk):
    session_data=User.objects.get(email=request.session["email"])
    myproduct=Product.objects.get(id=pk)
    try:
        mycart=Cart.objects.get(Q(product=myproduct) & Q(buyer=session_data))
        mycart.qty+=1
        mycart.total=mycart.qty*mycart.product.price
        mycart.save()
    except:
        Cart.objects.create(
            product=myproduct,
            buyer=session_data,
            qty=1,
            total=myproduct.price*1
        )
    # return shop(request)
    return redirect('shop')


def showcart(request):
    session_data=User.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer=session_data)
    final_total=0
    for i in all_cart:
        final_total+=i.total
    return render(request,"cart.html",{"all_cart":all_cart,"session_data":session_data,"final_total":final_total})


def update_cart(request):
    if request.method=="POST":
        session_data=User.objects.get(email=request.session["email"])
        all_cart=Cart.objects.filter(buyer=session_data)
        all_qty=request.POST.getlist("quantity")
        for i,j in zip(all_cart,all_qty):
            i.qty=int(j)
            i.total=i.qty*i.product.price
            i.save()
        # return showcart(request)
        return redirect('showcart')
    
def remove_cart(request,pk):
    one_cart=Cart.objects.get(id=pk)
    one_cart.delete()
    return redirect('showcart')
    
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
    
def search(request):
    if request.method=="POST":
        data=request.POST["ser"]
        all_product=Product.objects.filter(Q(pname__icontains=data)|Q(desc__icontains=data))
        session_data=User.objects.get(email=request.session["email"])
        return render(request,"shop.html",{"all_product":all_product,"session_data":session_data})
    else:
        return redirect('shop')