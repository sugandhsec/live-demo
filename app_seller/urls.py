from django.urls import path
from . import views

urlpatterns = [
   path('', views.seller_index, name='seller_index'),
   path('seller_register/', views.seller_register, name='seller_register'),
   path('seller_otp/', views.seller_otp, name='seller_otp'),
   path('seller_login/', views.seller_login, name='seller_login'),
   path('seller_logout/', views.seller_logout, name='seller_logout'),
   path('seller_profile/', views.seller_profile, name='seller_profile'),
   path('add_product/', views.add_product, name='add_product'),
   
  
   

]