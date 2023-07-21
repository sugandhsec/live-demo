from django.db import models

# Create your models here.
class Seller_User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    propic=models.FileField(upload_to="seller_profile/",default="anonymous.jpg")
    
    def __str__(self):
        return self.email
    
    
class Product(models.Model):
    pname=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    pimage =models.FileField(upload_to="seller_profile/",default="anonymous.jpg")
    desc  =models.CharField(max_length=500)
    qty =models.IntegerField(default=0)
    seller=models.ForeignKey(Seller_User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.pname