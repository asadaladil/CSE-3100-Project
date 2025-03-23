from django.db import models
from django.contrib.auth.models import User
from .constants import *
# Create your models here.

class UserRegisterModel(models.Model):
    # personal information and Password
    user=models.OneToOneField(User,related_name='Accounts',on_delete=models.CASCADE)
    phone=models.CharField(max_length=11)
    photo=models.ImageField(upload_to="profile_photos/")
    notify=models.JSONField(default=list)
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
    statement=models.JSONField(default=list
        # Date=models.DateTimeField(auto_now_add=True),
        # Description=models.CharField(max_length=30),
        # tran_type=models.CharField(max_length=20),
        # Amount=models.IntegerField(),
        # left_balance=models.IntegerField()
        )
    
    def __str__(self):
        name=self.user.first_name+' '+self.user.last_name
        return f"Account No: {self.user.username} ----- Name: {name}"
    

    