from operator import le
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from accounts.models import *
from accounts.forms import FPPageForm, FPform, PasswordChangeForm
from django.contrib import messages
from accounts.constants import *
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from django.utils import timezone
import os


def note(id):
    acc=UserRegisterModel.objects.get(user_id=id)
    notify=acc.notify[0][0]
    pic=acc.photo
    return [notify,pic]

def homepage(request):
    if request.user.is_authenticated: 
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        return render(request,'home.html',{'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    return render(request,'home.html')

def Change_Password(request):
    if request.user.is_authenticated:
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        if request.method == 'POST':
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            pass3=request.POST.get('pass3')
            if pass1==pass2 and pass2==pass3:
                messages.error(request,"Old and New Password must be different!!")
                return redirect('/password/')
            if acc.user.check_password(pass1)==False:
                messages.error(request,"Old Password is incorrect!!")
                return redirect('/password/')
            if pass2!=pass3:
                messages.error(request,"New Password and Confirm Password must be same!!")
                return redirect('/password/')
            acc.user.set_password(pass2)
            acc.user.save()
            messages.success(request,"Password Changed Successfully!!")
            messages.success(request,"You are SIGNED OUT. Enter Again? Then go to SIGN IN PAGE !!")
            return redirect('/')
        form=PasswordChangeForm()
        return render(request,'password.html',{'forms':form,'notify':note(request.user.id)[0],
                                               'pic':note(request.user.id)[1]})

def Delete_Page(request):
    if request.user.is_authenticated:
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        return render(request,"delete.html",{'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    return render(request,"page404.html")

def Delete(request):
    if request.user.is_authenticated:
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        file_path=str(acc.photo)
        if file_path:
            full_path=os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        logout(request)
        acc.user.delete()  
        messages.success(request,"Account is Deleted Successfully!")
        return redirect('/') 
    else:
        return render(request,"page404.html") 

def forgot_page(request):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        acc=UserRegisterModel.objects.all()
        user=request.POST.get('Account')
        v=0
        for i in acc:
            if i.user.username==user:
                v=1
                acc=i
                break
        if v==0:
            messages.error(request,"Account Does not Exist !!")
            return redirect('/forgot/')
        acc.OTP=make_otp()
        acc.save()
        return redirect(f'/Forgot/{user}')
    form=FPform()
    return render(request,"forgot.html",{'forms':form})

def Forgot(request,id):
    if request.user.is_authenticated:
        return render(request,"page404.html")
    if request.method=='POST':
        pin=request.POST.get('otp')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        acc=UserRegisterModel.objects.get(user__username=id)
        if pin!=acc.OTP:
            messages.error(request,"Invalid OTP !!")
            return redirect(f'/forgot/')
        if pass1!=pass2:
            messages.error(request,"Password Does not Match !!")
            return redirect(f'/forgot/')
        acc.user.set_password(pass1)
        acc.user.save()
        messages.success(request,"Password is Changed Successfully !!")
        return redirect('/accounts/login/')
    form=FPPageForm()
    acc=UserRegisterModel.objects.all()
    for i in acc:
        if i.user.username==id:
            acc=i
            break
    return render(request,"forgot2.html",{'forms':form,'pin':acc.OTP,'email':acc.user.email,'id':acc.user.username})



def PDF(request):
    if request.user.is_authenticated:
        acc=TransactionModel.objects.get(user_id=request.user.id)
        tm=timezone.now()-acc.user.last_login
        if tm.total_seconds()>600:
            messages.info(request,"Account is Logged out Due to accessing the A/C more than 10 minutes")
            logout(request)
            return redirect('/accounts/login/')
        data = [["Date-Time", "Description", "Specific Task","Amount","Balance After Transaction"]]
        
        for i in range(1,len(acc.statement)+1):
            data.append(acc.statement[-i])
        # Create a BytesIO buffer to hold the PDF
        buffer = BytesIO()
    # Create the document (landscape if desired)
        doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        title="Report",  # Set the PDF metadata title
        )
        
        styles = getSampleStyleSheet()
        elements = []
        
        centered_style = ParagraphStyle(
        name='CenteredTitle',
        parent=styles['Heading1'],
        alignment=1,
        fontSize=20,
        textColor='navy'
        )
        # Add a title
        elements.append(Paragraph("MyExpense Transaction Report", centered_style))
        elements.append(Paragraph(f"A/C No-{acc.user.username}", styles['Heading2']))
        elements.append(Paragraph(f"A/C Name: {acc.user.first_name} {acc.user.last_name}", styles['Heading2']))
        elements.append(Spacer(1, 5))
         
        
        # Create the table and apply a style
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        
        elements.append(table)
        
        # Build the PDF
        doc.build(elements)
        
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="Expense_Report.pdf"'
        response.write(pdf)
        return response