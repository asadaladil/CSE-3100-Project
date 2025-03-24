from django.forms import * 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import TransactionModel, UserRegisterModel
from django.contrib.auth.models import User
from django.core import validators
from .constants import *


class TransactionForm(Form):
    type=ChoiceField(label="Type Of Transaction",
                   help_text="Choose your Transaction",
                   choices=Description
                   )
    Amount=IntegerField(help_text="Enter your Amount")
    
    def clean_Amount(self):
        if self.cleaned_data['Amount']<0:
            raise ValidationError("Amount cannot be negative")
    

class FundTransferForm(Form):
    Account=CharField(help_text="Enter Account No of the Receiver",max_length=10,label="Account No")
    Amount=IntegerField(help_text="Enter your Amount")
    
    def clean_Account(self):
        val=self.cleaned_data['Account']
        acc=UserRegisterModel.objects.all()
        a=0
        for i in acc:
            if i.user.username==str(val):
                a=1
                break
        if a==0:
            raise ValidationError("Account No does not exist")
        
    def clean_Amount(self):
        if self.cleaned_data['Amount']<0:
            raise ValidationError("Amount cannot be negative")
    

        

class UserRegisterForm(UserCreationForm):
    Check=CharField(widget=CheckboxInput,label="Show Password",required=False)
    phone=CharField(max_length=11,help_text="Enter your Phone Number",required=False)
    File=FileField(help_text="Upload your Photo",required=False,validators=[validators.FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
    # Personal Address
    Country=ChoiceField(choices=country(),help_text="Select your Country")
    city=CharField(max_length=50,help_text="Enter your City")
    Address=CharField(max_length=200,help_text="Enter your Street Address")
    postal=IntegerField(help_text="Enter your Postal Code")
    class Meta:
        model = User
        fields=['password1', 'password2', 'first_name', 'last_name', 'email', 'File', 'postal', 'city','Country', 'Address']

        help_texts={
            'password1': "Enter your Password",
            'password2': "Enter your Password Again",
            'first_name':"Enter your First Name",
            'last_name':"Enter your Last Name",
            'email':"Enter your Email Address"
        }
        labels={
            'password2':"Confirm Password",
        }
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError("Password and Confirm Password must be same")
            
    def save(self, commit=True):
        new_user = super().save(commit=False) # ami database e data save korbo na ekhn
        
        if commit == True:
            id=UserRegisterModel.objects.last().user.username
            new_user.username=str(int(id)+1)
            new_user.is_staff=True
            new_user.save() # user model e data save korlam
            Postal= self.cleaned_data.get('postal')
            country = self.cleaned_data.get('Country')
            City = self.cleaned_data.get('city')
            address = self.cleaned_data.get('Address')
            Phone = self.cleaned_data.get('phone')
            file=self.cleaned_data.get('File')
            note=[[0]]
            
            TransactionModel.objects.create(
                user = new_user,
                
            )
            UserRegisterModel.objects.create(
                user=new_user,
                postal=Postal,
                Country=country,
                city=City,
                Address=address,
                phone=Phone,
                photo=file,
                notify=note
            )
        return new_user
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
                
    #             'class' : (
    #                 'appearance-none block w-full bg-gray-200 '
    #                 'text-gray-700 border border-gray-200 rounded '
    #                 'py-3 px-4 leading-tight focus:outline-none '
    #                 'focus:bg-white focus:border-gray-500'
    #             ) 
    #         })
            
class UserLoginForm(Form):
    Account_No=CharField(max_length=10,help_text="Enter your Account No",label="Account No:")
    Password=CharField(widget=PasswordInput,help_text="Enter your Password")
    Check=CharField(widget=CheckboxInput,required=False,label="Show Password")
    
# class UserUpdateForm(UserCreationForm):
#     phone=CharField(max_length=11,help_text="Enter your Phone Number")
#     File=FileField(help_text="Upload your Photo",required=False,validators=[validators.FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
#     # Personal Address
#     Country=ChoiceField(choices=country(),help_text="Select your Country")
#     city=CharField(max_length=50,help_text="Enter your City")
#     Address=CharField(max_length=200,help_text="Enter your Street Address")
#     postal=IntegerField(help_text="Enter your Postal Code")
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # for field in self.fields:
#         #     self.fields[field].widget.attrs.update({
#         #         'class': (
#         #             'appearance-none block w-full bg-gray-200 '
#         #             'text-gray-700 border border-gray-200 rounded '
#         #             'py-3 px-4 leading-tight focus:outline-none '
#         #             'focus:bg-white focus:border-gray-500'
#         #         )
#         #     })
#         # jodi user er account thake 
#         if self.instance:
#             try:
#                 user_account = self.instance
#                 user_info=self.instance.d
                
#             except UserRegisterModel.DoesNotExist:
#                 user_account = None

#             if user_account:
#                 self.fields['first_name'].initial = user_account.first_name
#                 self.fields['last_name'].initial = user_account.last_name
#                 self.fields['email'].initial = user_account.email
#                 #self.fields['Country'].initial = user_account.Country

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             user_account, created = UserRegisterModel.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            
#             user_account.Address = self.cleaned_data['Address']
#             user_account.city = self.cleaned_data['city']
#             user_account.postal = self.cleaned_data['postal']
#             user_account.Country = self.cleaned_data['Country']
#             user_account.save()

#         return user
    