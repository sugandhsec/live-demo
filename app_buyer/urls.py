"""
URL configuration for pro_ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('register/', views.register, name='register'),
   path('otp/', views.otp, name='otp'),
   path('login/', views.login, name='login'),
#    path('login/<str:mymsg>', views.login_msg, name='login'),
   path('logout/', views.logout, name='logout'),
   path('profile/', views.profile, name='profile'),
   path('shop/', views.shop, name='shop'),
   path('showcart/', views.showcart, name='showcart'),
   path('search/', views.search, name='search'),
   path('update_cart/', views.update_cart, name='update_cart'),
   path('single_product/<int:pk>', views.single_product, name='single_product'),
   path('remove_cart/<int:pk>', views.remove_cart, name='remove_cart'),
   path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
   path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
   
   

]
