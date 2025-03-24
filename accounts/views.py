from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import *
from .models import *
from .constants import *
import time


def note(id):
    return (UserRegisterModel.objects.get(user_id=id).notify[0][0])
def set_message(user_nm,ac_no2,amt):
    acc=UserRegisterModel.objects.all()
    acc2=TransactionModel.objects.all()
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
    for i in acc2:
        if i.user.username==ac_no2:
            i.bank+=int(amt)
            i.statement.append(set_statement(i,'Check Received',amt))
            if len(i.statement)>30:
                i.statement.pop(0)
            i.save()
            break
    return

def set_statement(acc,type,amnt):
    a=str(time.ctime())
    b=type
    c=amnt
    d=f"Bank Balance-->TK {acc.bank}\nCash Balance-->TK {acc.cash}"
    return [a,b,c,d]

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
                acc=TransactionModel.objects.get(user_id=request.user.id)
                temp=form.cleaned_data['type']
                money=int(request.POST.get('Amount'))
                if temp=='Check Deposit':
                    acc.bank+=money
                if temp=='Cash Deposit' and acc.cash>money:
                    if acc.cash<money:
                        messages.error(request,f"You don't have enough Cash to deposit TK-{money} !!")
                        return redirect('/accounts/transaction/')    
                    acc.bank+=money
                    acc.cash-=money
                if temp=='Cash Withdraw':
                    if acc.bank<money:
                        messages.error(request,f"You don't have enough Bank Balance to Withdraw TK-{money} !!")
                        return redirect('/accounts/transaction/')
                    acc.bank-=money
                    acc.cash+=money
                if temp=='Cash Income':
                    acc.cash+=money
                if temp=='Cash Expense':
                    if acc.cash<money:
                        messages.error(request,f"You don't have enough Cash to Expense TK-{money} !!")
                        return redirect('/accounts/transaction/')
                    acc.cash-=money
                acc.statement.append(set_statement(acc,temp,money))
                if len(acc.statement)>30:
                    acc.statement.pop(0)
                acc.save()
                messages.success(request,"Transaction is Successfully DONE!!")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,form.errors)
                return redirect('/accounts/transaction/')
        form=TransactionForm()
        return render(request,"transaction.html",{'forms':form,'notify':note(request.user.id)})
    else:
        return render(request,"page404.html") 


def FundTransfer(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=FundTransferForm(request.POST)
            if form.is_valid():
                acc=TransactionModel.objects.get(user_id=request.user.id)
                if acc.user.username==str(request.POST.get('Account')):
                    messages.error(request,"You can't Transfer your fund to your own Account")
                    return redirect('/accounts/transfer/')
                if acc.bank>int(request.POST.get('Amount')):
                    acc.bank-=int(request.POST.get('Amount'))
                else:
                    messages.error(request,"You don't have enough Bank Balance to Transfer!!")
                    return redirect('/accounts/transfer/')
                set_message(request.user.username,request.POST.get('Account'),request.POST.get('Amount'))
                acc.statement.append(set_statement(acc,'Check Pass',request.POST.get('Amount')))
                if len(acc.statement)>30:
                    acc.statement.pop(0)
                acc.save()
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


def cost(request):
    if request.user.is_authenticated:
        state=[]
        acc=TransactionModel.objects.get(user_id=request.user.id).statement
        for i in acc:
            if i[1]=='Cash Expense' or i[1]=='Check Pass':
                state.append(i)
        state.reverse()
        return render(request,"statements.html",{'cost':state,'count':len(state),'notify':note(request.user.id)})
    else:
        return render(request,"page404.html")

def income(request):
    if request.user.is_authenticated:
        state=[]
        acc=TransactionModel.objects.get(user_id=request.user.id).statement
        for i in acc:
            if i[1]!='Cash Expense' and i[1]!='Check Pass':
                state.append(i)
        state.reverse()
        return render(request,"statements.html",{'income':state,'count':len(state),'notify':note(request.user.id)})
    else:
        return render(request,"page404.html")

def alls(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id).statement
        acc.reverse()
        return render(request,"statements.html",{'state':acc,'count':len(acc),'notify':note(request.user.id)})
    else:
        return render(request,"page404.html")