from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField
from .constants import *
# Create your models here.

class UserRegisterModel(models.Model):
    # personal information and Password
    user=models.OneToOneField(User,related_name='Accounts',on_delete=models.CASCADE)
    phone=models.CharField(max_length=11)
    photo=models.ImageField(upload_to="profile_photos/",default=' ')
    notify=models.JSONField(default=list)
    OTP=models.CharField(max_length=6,default='0')
    # Personal Address
    Country=models.CharField(max_length=32,choices=country())
    city=models.CharField(max_length=50)
    Address=models.CharField(max_length=200)
    postal=models.IntegerField()
    
    def __str__(self):
        name=str(self.user.first_name+' '+self.user.last_name)
        return f"Account No: {self.user.username} ----- Name: {name}"

class TransactionModel(models.Model):
    user=models.OneToOneField(User,related_name='Transactions',on_delete=models.CASCADE)
    statement=models.JSONField(default=list)
    cash=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    bank=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    cost=models.JSONField(default=list)
    income=models.JSONField(default=list)
    
    def __str__(self):
        name=self.user.first_name+' '+self.user.last_name
        return f"Account No: {self.user.username} ----- Name: {name}"
    

    