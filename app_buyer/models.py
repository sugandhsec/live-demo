from django.db import models
from app_seller.models import *
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    propic=models.FileField(upload_to="user_profile/",default="anonymous.jpg")
    
    def __str__(self):
        return self.email
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    total=models.IntegerField(default=0)
    def __str__(self):
        return str(self.qty)
    