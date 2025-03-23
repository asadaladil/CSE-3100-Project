
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from .models import *
from .constants import *
import time


def note(id):
    return (UserRegisterModel.objects.get(user_id=id).notify[0][0])
def set_message(user_nm,ac_no2,amt):
    acc=UserRegisterModel.objects.all()
    for i in acc:
        if i.user.username==ac_no2:
            i.notify[0][0]+=1
            x=str(time.ctime())
            y=f"You Get Fund from the Account No- {user_nm}"
            z=amt
            i.notify.append([x,y,z])
            if len(i.notify)>11:
                i.notify.pop(1)
            i.save()
            break
    return

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            id=UserRegisterModel.objects.last().user.username
            messages.success(request,f"Account is Created Successfully----Your Account No: {id}")
            return redirect('/accounts/login/')
        else:
            #print(form.errors)
            return render(request,"register.html",context={'forms':form,'error':form.errors})
    form=UserRegisterForm()
    return render(request,"register.html",context={'forms':form})

    
def Login(request):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            user_ac=request.POST.get('Account_No')
            Pass=request.POST.get('Password')
            user=authenticate(request,username=user_ac,password=Pass)
            if user is not None:
                login(request,user)
                messages.success(request,"Account LOG IN Successfully!!")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,'Invalid Account No or Password!!')
                return redirect('/accounts/login/')
    form=UserLoginForm()
    return render(request,"login.html",context={'forms':form})

def logout_page(request):
    if request.user.is_authenticated:
        return render(request,"logout.html",{'notify':note(request.user.id)})
    return render(request,"page404.html")

def Logout(request):
    if request.user.is_authenticated:
        logout(request)  
        messages.success(request,"Account LOG OUT Successfully!")
        return redirect('/') 
    else:
        return render(request,"page404.html") 
       

def dashboard(request):
    if request.user.is_authenticated: 
        name=request.user.first_name+' '+request.user.last_name
        return render(request,"Dashboard.html",{'name':name,'notify':note(request.user.id)})
    elif request.method=='GET':
        return render(request,"page404.html")


def profile(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            ac=UserRegisterModel.objects.get(user_id=request.user.id)
            form1=UserRegisterForm(instance=request.user)
            form2=UserRegisterForm(instance=ac)
            # request.user dile nam email jay ar ac dile bakigule zay
            name=request.user.first_name+' '+request.user.last_name
            return render(request,"profile.html",context={'forms1':form1,'forms2':form2,'id':request.user.username
                                                          ,'name':name,'notify':note(request.user.id)})
        elif request.method=='POST':
            ac=UserRegisterModel.objects.get(user_id=request.user.id)
            ac.user.first_name=request.POST.get('first_name')
            ac.user.last_name=request.POST.get('last_name')
            ac.user.email=request.POST.get('email')
            ac.phone=request.POST.get('phone')
            ac.city=request.POST.get('city')
            ac.Country=request.POST.get('Country')
            ac.postal=request.POST.get('postal')
            ac.photo=request.POST.get('photo')
            ac.user.save()
            ac.save()
            form1=UserRegisterForm(instance=request.user)
            form2=UserRegisterForm(instance=ac)
            # request.user dile nam email jay ar ac dile bakigule zay
            name=request.user.first_name+' '+request.user.last_name
            messages.success(request,'Account Updated Successfully')
            return redirect('/accounts/dashboard/')
        return redirect('/accounts/login/') 
    else:
        return render(request,"page404.html") 
        

def transaction(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                messages.success(request,"Transaction is Successfully DONE!!")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,form.errors)
                return redirect('/accounts/transfer/')
        form=TransactionForm()
        return render(request,"transaction.html",{'forms':form,'notify':note(request.user.id)})
    else:
        return render(request,"page404.html") 


def FundTransfer(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=FundTransferForm(request.POST)
            if form.is_valid():
                set_message(request.user.username,request.POST.get('Account'),request.POST.get('Amount'))
                messages.success(request,"Fund Transfer Successfully from your Bank")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,form.errors)
                return redirect('/accounts/transfer/')
        form=FundTransferForm()
        return render(request,"transfer.html",{'forms':form,'notify':note(request.user.id)})
    else:
        return render(request,"page404.html") 

def notification(request):
    if request.user.is_authenticated:
        ac=UserRegisterModel.objects.get(user_id=request.user.id)
        no=ac.notify[0][0]
        new_note=[]
        old_note=[]
        for i in range(1,no+1):
            new_note.append(ac.notify[-i])
        for i in range(1,len(ac.notify)):
            old_note.append(ac.notify[-i])
        ac.notify[0][0]=0
        ac.save()
        return render(request,"notification.html",{'notify':note(request.user.id),'new_note':new_note,'note':no,
                                                   'notes':old_note,'prv':len(ac.notify)-1})
    else:
        return render(request,"page404.html")

