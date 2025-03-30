from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.contrib import messages
from django.conf import settings
from .forms import *
from .models import *
from .constants import *
import time
from django.utils import timezone
import os

def note(id):
    acc=UserRegisterModel.objects.get(user_id=id)
    notify=acc.notify[0][0]
    pic=acc.photo
    return [notify,pic]
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
            Savings(i,['income','Get Fund',int(amt)])
            i.statement.append(set_statement(i,'Check Received','Income',amt))
            if len(i.statement)>30:
                i.statement.pop(0)
            i.save()
            break
    return
def set_statement(acc,type,specific,amnt):
    a=str(time.ctime())
    b=type
    c=amnt
    d=f"Bank Balance-->TK {acc.bank}__Cash Balance-->TK {acc.cash}"
    return [a,b,specific,c,d]
def Savings(acc,List):
    a=0
    if List[0]=='cost':
        for i in range(0,len(acc.cost)):
            if acc.cost[i][0]==List[1]:
                acc.cost[i][1]+=List[2]
                a=1
                break
        if a==0:
            acc.cost.append([List[1],List[2]])
        acc.cost.sort()
        acc.save()
        return
    a=0    
    if List[0]=='income':
        for i in range(0,len(acc.income)):
            if acc.income[i][0]==List[1]:
                acc.income[i][1]+=List[2]
                a=1
                break
        if a==0:
            acc.income.append([List[1],List[2]])
        acc.income.sort()
        acc.save()
        return

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        form=UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            acc=UserRegisterModel.objects.last()
            id=acc.user.username
            pin=make_otp()
            acc.OTP=int(pin)
            acc.save()
            messages.success(request,f"Account is Created Successfully!!")
            messages.info(request,f"Your Account No- {id}")
            messages.info(request,f"Go to Verify Page for Verification!!")
            messages.info(request,f"OTP {pin} is sent to {acc.user.email}")
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
            acc=UserRegisterModel.objects.all()
            v=0
            for i in acc:
                if i.user.username==user_ac:
                    v=1
                    acc=i
                    break
            if v==0:
                messages.error(request,'Account No Does not Exist!!')
                return redirect('/accounts/login/')
            if acc.OTP!='0' and user is not None:
                messages.info(request,"Go to Verify page for Verification")
                acc.OTP=make_otp()
                acc.save()
                messages.info(request,f"OTP {acc.OTP} is sent to {acc.user.email}")
                return redirect('/accounts/login/')
            if user is not None:
                login(request,user)
                messages.success(request,"Account LOG IN Successfully!!")
                return redirect('/accounts/dashboard/')   
            else:
                messages.error(request,'Your Password is WRONG !!')
                return redirect('/accounts/login/')
    form=UserLoginForm()
    return render(request,"login.html",context={'forms':form})

def logout_page(request):
    if request.user.is_authenticated:
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        return render(request,"logout.html",{'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
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
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            acc.cost=[]
            acc.income=[]
            acc.bank=0
            acc.cash=0
            acc.save()
            messages.success(request,"RESET is DONE Successfully!!")
            return redirect('/accounts/dashboard/')
        hand=acc.cash
        bank=acc.bank
        Income=0
        Cost=0
        for i in acc.cost:
            Cost+=i[1]
        for i in acc.income:
            Income+=i[1]
        Save=hand+bank
        cp,sp=0,0
        if Income!=0:
            cp=round((Cost/Income)*100,2)
            sp=100-cp
        chart1=BarGraph(acc.income,Income,'Income')
        chart2=BarGraph(acc.cost,Cost,'Cost')
        chart3=PieGraph(Income,Cost)
        name=acc.user.first_name+' '+acc.user.last_name
        return render(request,"Dashboard.html",{'name':name,'notify':note(request.user.id)[0],'ac':acc.user.username,
                                                'bank':bank,'hand':hand,'cost':Cost,'income':Income,'save':Save,
                                                'cp':cp,'sp':sp,'nm':'cost','pic':note(request.user.id)[1],
                                                'chart1':chart1,'chart2':chart2,'chart3':chart3})
    else:
        return render(request,"page404.html")


def profile(request):
    if request.user.is_authenticated:
        ac=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-ac.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            # ac=UserRegisterModel.objects.get(user_id=request.user.id)
            ac.user.first_name=request.POST.get('first_name')
            ac.user.last_name=request.POST.get('last_name')
            ac.user.email=request.POST.get('email')
            ac.phone=request.POST.get('phone')
            ac.city=request.POST.get('city')
            ac.Country=request.POST.get('Country')
            ac.postal=request.POST.get('postal')
            ac.Address=request.POST.get('Address')
            file_path=str(ac.photo)
            if file_path and request.FILES.get('File'):
                full_path=os.path.join(settings.MEDIA_ROOT, file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
            if request.FILES.get('File'):
                ac.photo=request.FILES.get('File')
            ac.user.save()
            ac.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect('/accounts/dashboard/')
            
        # ac=UserRegisterModel.objects.get(user_id=request.user.id)
        form=UserUpdateForm(instance=ac)
        name=ac.user.first_name+' '+ac.user.last_name
        return render(request,"profile.html",context={'id':ac.user.username,
                                                    'name':name,'notify':note(request.user.id)[0],
                                                    'forms':form,'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html") 
        

def transaction(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                temp=form.cleaned_data['type']
                money=int(request.POST.get('Amount'))
                specific=request.POST.get('Specific')
                if temp=='Check Deposit':
                    acc.bank+=money
                    Savings(acc,['income',specific,money])
                if temp=='Cash Deposit':
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
                    Savings(acc,['income',specific,money])
                if temp=='Cash Expense':
                    if acc.cash<money:
                        messages.error(request,f"You don't have enough Cash to Expense TK-{money} !!")
                        return redirect('/accounts/transaction/')
                    acc.cash-=money
                    Savings(acc,['cost',specific,money])
                acc.statement.append(set_statement(acc,temp,specific,money))
                if len(acc.statement)>30:
                    acc.statement.pop(0)
                acc.save()
                messages.success(request,"Transaction is Successfully DONE!!")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,form.errors)
                return redirect('/accounts/transaction/')
        form=TransactionForm()
        return render(request,"transaction.html",{'forms':form,'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html") 


def FundTransfer(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            form=FundTransferForm(request.POST)
            if form.is_valid():
                if acc.user.username==str(request.POST.get('Account')):
                    messages.error(request,"You can't Transfer your fund to your own Account")
                    return redirect('/accounts/transfer/')
                if acc.bank>=int(request.POST.get('Amount')):
                    acc.bank-=int(request.POST.get('Amount'))
                    Savings(acc,['cost','Payment',int(request.POST.get('Amount'))])
                else:
                    messages.error(request,"You don't have enough Bank Balance to Transfer!!")
                    return redirect('/accounts/transfer/')
                set_message(acc.user.username,request.POST.get('Account'),request.POST.get('Amount'))
                acc.statement.append(set_statement(acc,'Check Pass','Payment',request.POST.get('Amount')))
                if len(acc.statement)>30:
                    acc.statement.pop(0)
                acc.save()
                messages.success(request,"Fund Transfer Successfully from your Bank")
                return redirect('/accounts/dashboard/')
            else:
                messages.error(request,form.errors)
                return redirect('/accounts/transfer/')
        form=FundTransferForm()
        return render(request,"transfer.html",{'forms':form,'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html") 

def notification(request):
    if request.user.is_authenticated:
        ac=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-ac.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            ac.notify=[[0]]
            ac.save()
        no=ac.notify[0][0]
        new_note=[]
        old_note=[]
        for i in range(1,no+1):
            new_note.append(ac.notify[-i])
        for i in range(1,len(ac.notify)):
            old_note.append(ac.notify[-i])
        ac.notify[0][0]=0
        ac.save()
        return render(request,"notification.html",{'notify':note(request.user.id)[0],'new_note':new_note,'note':no,
                                                   'notes':old_note,'prv':len(ac.notify)-1,
                                                   'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html")


def cost(request):
    if request.user.is_authenticated:
        state=[]
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        for i in acc.statement:
            if i[1]=='Cash Expense' or i[1]=='Check Pass':
                state.append(i)
        state.reverse()
        return render(request,"statements.html",{'cost':state,'count':len(state),'notify':note(request.user.id)[0],
                                                 'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html")

def income(request):
    if request.user.is_authenticated:
        state=[]
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        for i in acc.statement:
            if i[1]!='Cash Expense' and i[1]!='Check Pass':
                state.append(i)
        state.reverse()
        return render(request,"statements.html",{'income':state,'count':len(state),'notify':note(request.user.id)[0],
                                                 'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html")

def alls(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            acc.statement=[]
            acc.save()
        acc.statement.reverse()
        return render(request,"statements.html",{'state':acc.statement,'count':len(acc.statement),'notify':note(request.user.id)[0],
                                                 'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html")

def update_specific(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method=='POST':
            
            temp=request.POST.get('Type')
            temp1=request.POST.get('type')
            cat=request.POST.get('Specific')
            amt=int(request.POST.get('Amount'))
            if amt<0:
                messages.error(request,"Amount Can't be Negative")
                return redirect('/accounts/specific/')
            if temp=='Cost':
                if temp1=='Cash Expense' or temp1=='Check Pass':
                    v=0
                    for i in acc.cost:
                        if i[0]==cat:
                            v=1
                            dif=(i[1]-amt)
                            if temp1=='Cash Expense':
                                if (acc.cash+dif)<0:
                                    messages.error(request,f"Insufficient Cash Balance to deduct {abs(dif)} from{acc.cash}")
                                    return redirect('/accounts/specific/')
                                i[1]=amt
                                acc.cash+=dif
                                acc.save()
                                messages.success(request,f"Value Updated Successfully!!")
                                return redirect('/accounts/dashboard/')
                            elif temp1=='Check Pass':
                                if (acc.bank+dif)<0:
                                    messages.error(request,f"Insufficient Bank Balance to deduct {abs(dif)} from{acc.bank}")
                                    return redirect('/accounts/specific/')
                                i[1]=amt
                                acc.bank+=dif
                                acc.save()
                                messages.success(request,f"Value Updated Successfully!!")
                                return redirect('/accounts/dashboard/')
                    if v==0:
                        messages.error(request,f"Category Not Found")
                        return redirect('/accounts/specific/')            
                else:
                    messages.error(request,f"Invalid selection {temp1} and {temp}")
                    return redirect('/accounts/specific/')
            elif temp=='Income':
                if temp1=='Check Deposit' or temp1=='Cash Income':
                    v=0
                    for i in acc.income:
                        if i[0]==cat:
                            v=1
                            dif=(amt-i[1])
                            if temp1=='Check Deposit':
                                if (acc.bank+dif)<0:
                                    messages.error(request,f"Insufficient Bank Balance to deduct {abs(dif)} from{acc.bank}")
                                    return redirect('/accounts/specific/')
                                i[1]=amt
                                acc.bank+=dif
                                acc.save()
                                messages.success(request,f"Value Updated Successfully!!")
                                return redirect('/accounts/dashboard/')
                            elif temp1=='Cash Income':
                                if (acc.cash+dif)<0:
                                    messages.error(request,f"Insufficient Bank Balance to deduct {abs(dif)} from{acc.cash}")
                                    return redirect('/accounts/specific/')
                                i[1]=amt
                                acc.cash+=dif
                                acc.save()
                                messages.success(request,f"Value Updated Successfully!!")
                                return redirect('/accounts/dashboard/')
                    if v==0:
                        messages.error(request,f"Category Not Found")
                        return redirect('/accounts/specific/')            
                else:
                    messages.error(request,f"Invalid selection {temp1} and {temp}")
                    return redirect('/accounts/specific/')
        form=SpecificForm()
        return render(request,"specific.html",{'forms':form,'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    else:
        return render(request,"page404.html")

                       
def otp(request):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        user=request.POST.get('Account')
        acc=UserRegisterModel.objects.all()
        v=0
        for i in acc:
            if i.user.username==user:
                v=1
                acc=i
                break
        if v==0:
            messages.error(request,f"User Not Found")
            return redirect('/accounts/verify/')
        if acc.OTP=='0':
            messages.success(request,"Account is already verified !!")
            return redirect('/accounts/login/')
        if request.POST.get('otp')==acc.OTP:
            acc.OTP='0'
            acc.save()
            messages.success(request,"Account is verified Successfully!!")
            return redirect('/accounts/login/')
        else:
            messages.error(request,f"Invalid OTP")
            return redirect('/accounts/verify/')
    form=OTPForm()
    return render(request,"otp.html",{'forms':form})
                