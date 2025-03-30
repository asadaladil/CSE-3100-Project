from django.forms import * 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import TransactionModel, UserRegisterModel
from django.contrib.auth.models import User
from django.core import validators
from .constants import *

extention=['jpg','jpeg','png','JPG','JPEG','PNG']

class TransactionForm(Form):
    type=ChoiceField(label="Type Of Transaction",
                   help_text="Choose your Transaction",
                   choices=Description
                   )
    Specific=CharField(label="Specific type",help_text="Say About that Transaction",max_length=30)
    Amount=IntegerField(help_text="Enter your Amount")
    
    def clean_Amount(self):
        if self.cleaned_data['Amount']<=0:
            raise ValidationError("Amount cannot be negative or equal to 0")
    
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
        if self.cleaned_data['Amount']<=0:
            raise ValidationError("Amount cannot be negative or equal to 0")
    
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
    
class UserUpdateForm(UserCreationForm):
    phone=CharField(max_length=11,help_text="Enter your Phone Number")
    File=FileField(help_text="Upload your Photo",required=False,validators=[validators.FileExtensionValidator(allowed_extensions=extention)])
    # Personal Address
    Country=ChoiceField(choices=country(),help_text="Select your Country")
    city=CharField(max_length=50,help_text="Enter your City")
    Address=CharField(max_length=200,help_text="Enter your Street Address")
    postal=IntegerField(help_text="Enter your Postal Code")
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        user_account = self.instance
        self.fields['first_name'].initial=user_account.user.first_name
        self.fields['last_name'].initial=user_account.user.last_name
        self.fields['email'].initial=user_account.user.email
        self.fields['Country'].initial=user_account.Country
        self.fields['city'].initial=user_account.city
        self.fields['phone'].initial=user_account.phone
        self.fields['Address'].initial=user_account.Address
        self.fields['postal'].initial=user_account.postal
        self.fields['File'].initial=user_account.photo
    

added=(
    ('Check Deposit','Check Deposit'),
    ('Cash Deposit','Cash Deposit'),
    ('Cash Withdraw','Cash Withdraw'),
    ('Cash Income','Cash Income'),
    ('Cash Expense','Cash Expense'),
    ('Check Pass','Check Pass')   
)
class SpecificForm(Form):
    type=ChoiceField(label="Type Of Transaction",
                   help_text="Choose your Transaction",
                   choices=added
                   )
    Type=ChoiceField(choices=Type,help_text="Choose your Type")
    Specific=CharField(help_text='Enter the Category Name you want to Change')
    Amount=DecimalField(max_digits=20,decimal_places=2,help_text="Enter the Updated Amount")

class PasswordChangeForm(Form):
    pass1=CharField(widget=PasswordInput, help_text="Enter your Old Password",label="Old Password:")
    pass2=CharField(widget=PasswordInput,required=True,help_text="Enter your New Password",label="New Password:")
    pass3=CharField(widget=PasswordInput,required=True,help_text="Confirm your New Password Again",label="Confirm New Password:")
    Check=CharField(widget=CheckboxInput,required=False,label="Show Password")
    
class OTPForm(Form):
    Account=CharField(max_length=10,label="Account No:",help_text="Enter your Account No")
    otp=CharField(max_length=6,help_text="Enter your OTP",label="OTP")

class FPform(Form):
    Account=CharField(max_length=10,label="Account No:",help_text="Enter your Account No")
    
class FPPageForm(Form):
    otp=CharField(max_length=6,help_text="Enter your OTP",label="OTP")
    pass1=CharField(widget=PasswordInput,required=True,help_text="Enter your New Password",label="New Password:")
    pass2=CharField(widget=PasswordInput,required=True,help_text="Confirm your New Password Again",label="Confirm New Password:")
    Check=CharField(widget=CheckboxInput,required=False,label="Show Password")