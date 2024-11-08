from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import date,datetime,timedelta
from django.db.models import Q,Min,Count,Sum, F, Case, When, Value, CharField, BooleanField,OuterRef,FloatField,Exists,Subquery,Prefetch,JSONField
from django.middleware.csrf import get_token
from django.apps import apps
from email.message import EmailMessage
from django.db.models.functions import Concat,Cast
from dotenv import load_dotenv
import ssl
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import smtplib
import random
import string
import json
import os

load_dotenv() 

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def login(request):
    return render(request,'login.html')


def home(request):
    if 'login_id' in request.session:
        user = request.session['login_id']
        data = Login.objects.get(login_id=user)
        if data.user_type == 'admin':
            request.session['master'] = data.login_id
            return redirect('/master_home/')
        elif data.user_type == 'Accountant':
            use = Staff_register.objects.get(login_id=user)
            request.session['accountant'] = use.sr_id
            request.session['staff_id'] = use.sr_id
            return redirect('/accountant_home/')
        elif data.user_type == 'Office staff':
            use = Staff_register.objects.get(login_id=user)
            request.session['office_staff'] = use.sr_id
            request.session['staff_id'] = use.sr_id
            return redirect('/office_staff_home/')
        elif data.user_type == 'Faculty':
            use = Staff_register.objects.get(login_id=user)
            request.session['faculty'] = use.sr_id
            request.session['staff_id'] = use.sr_id
            return redirect('/faculty_home/')
        elif data.user_type == 'Student':
            use = Student_register.objects.get(login_id=user)
            request.session['student'] = use.sr_id
            return redirect('/student_home/')
        else:
            return redirect('/home/')  
    else:
        return render(request,'index.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            data = Login.objects.get(username=username,password= password)
            if data.status == True:
                request.session['login_id'] = data.login_id
                return redirect('/home/')
            else:
                messages.success(request,'Admin denial your access')
                return redirect('/login/')
        except Exception:
            messages.success(request, 'Invalid Email id Or Password')
            return redirect('/login/')
    else:
        return render(request,'login.html')
    
def master_home(request):
    return render(request,'master/index.html')

def accountant_home(request):
    return render(request,'accountant/index.html')

def office_staff_home(request):
    return render(request,'office_staff/index.html')

def faculty_home(request):
    return render(request,'faculty/index.html')

def student_home(request):
    return render(request,'student/index.html')

    
def leave_type(request):
    if 'master' in request.session:
        if request.method == 'POST':
            obj = Leave_type()
            obj.leave_type = request.POST['leave_type']
            obj.days = request.POST['days']
            obj.save()
            messages.success(request, 'Added successfully.')
            return redirect('/leave_type')
        else:
            data = Leave_type.objects.all()
            return render(request,'master/leave_type.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_leave_type(request):
    if 'master' in request.session:
        if request.method == 'POST':
            obj = Leave_type.objects.get(lt_id=request.POST['lt_id'])
            obj.days = request.POST['days']
            obj.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/leave_type')
        elif 'lt_id' in request.GET:
            data = Leave_type.objects.get(lt_id=request.GET['lt_id'])
            return render(request,'master/edit_leave_type.html',{'data':data})
        else:
            return redirect('/leave_type')
    else:
        return redirect('/home/')

def status_leave_type(request):
    if 'master' in request.session:
        data = Leave_type.objects.get(lt_id=request.GET['lt_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/leave_type')
    else:
        return redirect('/home/')  
    
def academic_year(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Academic_year()
            ob.academic_year = request.POST['academic_year']+"-" +str(int(request.POST['academic_year'])+1)
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/academic_year/')
        else:
            data = Academic_year.objects.all()
            return render(request,'master/academic_year.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_academic_year(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Academic_year.objects.get(ay_id=request.POST['ay_id'])
            ob.academic_year = request.POST['academic_year'] +"-" +str(int(request.POST['academic_year'])+1)
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/academic_year/')
        elif 'ay_id' in request.GET:
            data = Academic_year.objects.get(ay_id=request.GET['ay_id'])
            return render(request,'master/edit_academic_year.html',{'data':data})
        else:
            return redirect('/academic_year/')
    else:
        return redirect('/home/')

def status_academic_year(request):
    if 'master' in request.session:
        data = Academic_year.objects.get(ay_id=request.GET['ay_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/academic_year/')
    else:
        return redirect('/home/')

def update_current_ay(request):
    if 'master' in request.session:
        data = Academic_year.objects.get(ay_id=request.GET['ay_id'])
        data.current_ay = True
        data.save()
        Academic_year.objects.exclude(ay_id=request.GET['ay_id']).update(current_ay=False)
        messages.success(request, 'Updated successfully')
        return redirect('/academic_year/')
    else:
        return redirect('/home/')

def designation(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Designation()
            ob.designation_name = request.POST['designation_name']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/designation/')
        else:
            data = Designation.objects.all()
            return render(request,'master/designation.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_designation(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Designation.objects.get(d_id=request.POST['d_id'])
            ob.designation_name = request.POST['designation_name']
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/designation/')
        elif 'd_id' in request.GET:
            data = Designation.objects.get(d_id=request.GET['d_id'])
            return render(request,'master/edit_designation.html',{'data':data})
        else:
            return redirect('/designation/')
    else:
        return redirect('/home/')

def status_designation(request):
    if 'master' in request.session:
        data = Designation.objects.get(d_id=request.GET['d_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/designation/')
    else:
        return redirect('/home/')
    
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + '@#%!'
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
 
def staff_register(request):
    if request.method == 'POST':
        try:
            Login.objects.get(username=request.POST['username'])
            messages.success(request, 'This Username is already Exist.')
            return redirect('/staff_register/')
        except Exception:
            password = generate_password()
            email_sender=os.environ.get('EMAIL')    
            email_password=os.environ.get('EMAIL_PASSWORD') 
            email_receiver=request.POST['email']
            subject="School accounts management-password"
            
            body=f"Dear {request.POST['name']},\n\n The password for logging into the school accounts management system is: \nPassword: {password}"
            em=EmailMessage()
            em['From']=email_sender
            em['To']=email_receiver
            em['Subject']=subject
            em.set_content(body)
            context=ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            ob = Login()
            ob.username = request.POST['email']
            ob.password = password
            ob.user_type = request.POST['user_type']
            ob.save()

            d = Login.objects.get(username=request.POST['email'])

            obj = Staff_register()
            obj.name = request.POST['name']
            obj.designation_id = request.POST['designation_id']
            obj.login = d
            obj.save()
            messages.success(request, 'Registered successfully.')
            return redirect('/staff_register/')
    else:
        dt = Designation.objects.filter(status=True)
        return render(request,'master/staff_register.html',{'designation':dt})

def staff_status(request):
    if 'master' in request.session:
        data = Login.objects.get(login_id=request.GET['login_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/staff_list/')
    else:
        return redirect('/home/')

def student_register(request):
    if request.method == 'POST':
        try:
            Login.objects.get(username=request.POST['username'])
            messages.success(request, 'This Username is already Exist.')
            return redirect('/student_register/')
        except Exception:
            ob = Login()
            ob.username = request.POST['username']
            ob.password = request.POST['password']
            ob.user_type = 'Student'
            ob.save()

            d = Login.objects.get(username=request.POST['username'])

            obj = Student_register()
            obj.name = request.POST['name']
            obj.email = request.POST['email']
            obj.contact_number = request.POST['contact_number']
            obj.address = request.POST['address']
            obj.standard_id = request.POST['standard_id']
            obj.gender = request.POST['gender']
            obj.login = d
            if 'image' in request.FILES:
                im=request.FILES['image']
                ob = FileSystemStorage()
                fl = ob.save(im.name,im)
                
                obj.image = ob.url(fl)
            obj.save()
            messages.success(request, 'Registered successfully.')
            return redirect('/student_register/')
    else:
        dt = Standard.objects.select_related('educational_level')
        return render(request,'office_staff/student_register.html',{'standard':dt})


def student_list(request):
    if 'office_staff' in request.session:
        data = Student_register.objects.select_related('login','standard').order_by('-sr_id')
        return render(request,'office_staff/student_list.html',{'data':data})
    else:
        return redirect('/home/')
    
def student_status(request):
    if 'office_staff' in request.session:
        data = Login.objects.get(login_id=request.GET['login_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/student_list/')
    else:
        return redirect('/home/')

def leave_apply(request):
    if 'login_id' in request.session:
        if request.method == 'POST':
            obj = Staff_leave()
            obj.reason = request.POST['reason']
            obj.start_date = request.POST['start_date']
            obj.end_date = request.POST['end_date']
            obj.leave_type_id = request.POST['leave_type_id']
            
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            if start_date == end_date:
                no_of_days = 1
                obj.no_of_days = no_of_days
            else:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                no_of_days = (end_date_obj - start_date_obj).days + 1
                obj.no_of_days = no_of_days
            
            if 'accountant' in request.session:
                obj.staff_id = request.session['accountant']
            elif 'office_staff' in request.session:
                obj.staff_id = request.session['office_staff']
            elif 'faculty' in request.session:
                obj.staff_id = request.session['faculty']
            
            obj.save()
            messages.success(request, 'Submitted successfully.')
            return redirect('/leave_apply/')
        else:
            data = Leave_type.objects.all()
            if 'accountant' in request.session:
                return render(request,'accountant/leave_apply.html',{'data':data})
            elif 'office_staff' in request.session:
                return render(request,'office_staff/leave_apply.html',{'data':data})
            elif 'faculty' in request.session: 
                return render(request,'faculty/leave_apply.html',{'data':data})
            else:
                return redirect('/home/')
    else:
        return redirect('/home/')

def new_leave_request(request):
    if 'master' in request.session:
        data = Staff_leave.objects.filter(status=None)
        return render(request,'master/new_leave_request.html',{'data':data})
    else:
        return redirect('/home/')
    
def leave_status(request):
    if 'master' in request.session:
        if 'sl_id' in request.GET:
            obj = Staff_leave.objects.get(sl_id=request.GET['sl_id'])
            obj.status = request.GET['status']
            obj.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('/new_leave_request/')
        else:
            return redirect('/new_leave_request/')
    else:
        return redirect('/home/')

def leave_list(request):
    if 'accountant' in request.session:
        data = Staff_leave.objects.filter(staff_id=request.session['accountant']).order_by('-sl_id')
        return render(request,'accountant/leave_list.html',{'data':data})
    elif 'office_staff' in request.session:
        data = Staff_leave.objects.filter(staff_id=request.session['office_staff']).order_by('-sl_id')
        return render(request,'office_staff/leave_list.html',{'data':data})
    elif 'faculty' in request.session:
        data = Staff_leave.objects.filter(staff_id=request.session['faculty']).order_by('-sl_id')
        return render(request,'faculty/leave_list.html',{'data':data})
    elif 'master' in request.session:
        data = Staff_leave.objects.filter(~Q(status=None))
        return render(request,'master/leave_list.html',{'data':data})
    else:
        return redirect('/home/')


def profile(request):
    if 'login_id' in request.session:
        if request.method == 'POST':
            if 'accountant' in request.session:
                obj = Staff_register.objects.get(sr_id=request.session['accountant'])
            elif 'office_staff' in request.session:
                obj = Staff_register.objects.get(sr_id=request.session['office_staff'])
            elif 'faculty' in request.session:
                obj = Staff_register.objects.get(sr_id=request.session['faculty'])
            elif 'student' in request.session:
                obj = Student_register.objects.get(sr_id=request.session['student'])
                obj.gender = request.POST['gender']
                obj.email = request.POST['email']
            else:
                return redirect('/home/')
            
            obj.name = request.POST['name']
            obj.contact_number = request.POST['contact_number']
            obj.address = request.POST['address']
            if 'image' in request.FILES:
                im=request.FILES['image']
                ob = FileSystemStorage()
                fl = ob.save(im.name,im)
                
                obj.image = ob.url(fl)
            obj.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('/profile/')
        else:
            if 'accountant' in request.session:
                data = Staff_register.objects.get(sr_id=request.session['accountant'])
                return render(request,'accountant/profile.html',{'data':data})
            elif 'office_staff' in request.session:
                data = Staff_register.objects.get(sr_id=request.session['office_staff'])
                return render(request,'office_staff/profile.html',{'data':data})
            elif 'faculty' in request.session:
                data = Staff_register.objects.get(sr_id=request.session['faculty'])
                return render(request,'faculty/profile.html',{'data':data})
            elif 'student' in request.session:
                data = Student_register.objects.get(sr_id=request.session['student'])
                return render(request,'student/profile.html',{'data':data})
            else:
                return redirect('/home/')
    else:
        return redirect('/home/')


def staff_list(request):
    if 'master' in request.session:
        data = Staff_register.objects.select_related('login','designation')
        return render(request,'master/staff_list.html',{'data':data})
    else:
        return redirect('/home/')

def school_finance(request):
    data = School_finance.objects.all()
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = School_finance()
            ob.account_category = request.POST['account_category']
            ob.finance_type = request.POST['finance_type']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/school_finance/')
        else:
            income_records = School_finance.objects.filter(account_category='Income')
            expense_records = School_finance.objects.filter(account_category='Expense')

            return render(request, 'accountant/school_finance.html', {
                'income_records': income_records,
                'expense_records': expense_records
            })
    elif 'master' in request.session:
        return render(request,'master/school_finance.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_school_finance(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = School_finance.objects.get(sf_id=request.POST['sf_id'])
            ob.account_category = request.POST['account_category']
            ob.finance_type = request.POST['finance_type']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/school_finance/')
        else:
            data = School_finance.objects.get(sf_id=request.GET['sf_id'])
            return render(request,'accountant/edit_school_finance.html',{'data':data})
    else:
        return redirect('/home/')
    
def status_school_finance(request):
    if 'accountant' in request.session:
        data = School_finance.objects.get(sf_id=request.GET['sf_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/school_finance/')
    else:
        return redirect('/home/')

def salary_table(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = Salary_table()
            ob.account_category = request.POST['account_category']
            ob.designation_id = request.POST['designation_id']
            ob.da = request.POST['da']
            ob.ta = request.POST['ta']
            ob.hra = request.POST['hra']
            ob.agp = request.POST['agp']
            ob.basic_pay = request.POST['basic_pay']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/salary_table/')
        else:
            data = Salary_table.objects.select_related('designation')
            des = Designation.objects.filter(status=True)
            return render(request,'accountant/salary_table.html',{'data':data,'des':des})
    elif 'master' in request.session:
        data = Salary_table.objects.select_related('designation')
        return render(request,'master/salary_table.html',{'data':data})
    else:
        return redirect('/home/')

def edit_salary_table(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = Salary_table.objects.get(st_id=request.POST['st_id'])
            ob.account_category = request.POST['account_category']
            ob.designation_id = request.POST['designation_id']
            ob.da = request.POST['da']
            ob.ta = request.POST['ta']
            ob.hra = request.POST['hra']
            ob.agp = request.POST['agp']
            ob.basic_pay = request.POST['basic_pay']
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/salary_table/')
        else:
            data = Salary_table.objects.get(st_id=request.GET['st_id'])
            des = Designation.objects.all()
            return render(request,'accountant/edit_salary_table.html',{'data':data,'des':des})
    else:
        return redirect('/home/')
    
def status_salary_table(request):
    if 'accountant' in request.session:
        data = Salary_table.objects.get(st_id=request.GET['st_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/salary_table/')
    else:
        return redirect('/home/')
    
def student_fee(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = Student_fee()
            ob.account_category = request.POST['account_category']
            ob.educational_level_id = request.POST['educational_level_id']
            ob.fee_type = request.POST['fee_type']
            ob.amount = request.POST['amount']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/student_fee/')
        else:
            data = Student_fee.objects.select_related('educational_level')
            edl = Educational_level.objects.all()
            return render(request,'accountant/student_fee.html',{'data':data,'edl':edl})
    elif 'master' in request.session:
        data = Student_fee.objects.select_related('educational_level')
        return render(request,'master/student_fee.html',{'data':data})
    elif 'student' in request.session:
        if 'sf_id' in request.GET:
            current_date = date.today()
            current_year = current_date.year
            j = date(current_year, 6, 1)
            year_value = current_year if current_date >= j else current_year + 1
            fee = Student_fee.objects.get(sf_id=request.GET['sf_id'])

            ex = Academic_year.objects.filter(current_ay=True).exists()
            data = None
            if ex:
                try:
                    Academic_year.objects.get(academic_year__startswith=year_value, current_ay=True)
                    starting_date = datetime(year_value, 6, 1)
                    ending_date = datetime(year_value+1, 3, 30)

                    current = starting_date
                    months = []
                    while current <= ending_date and current <= datetime.today():
                        months.append((current.year, current.month))
                        current += timedelta(days=32)  
                        current = current.replace(day=1)
                    
                    
                    student_id = request.session['student']
                    student_fee_id = request.GET['sf_id']

                    transactions = (
                        Student_fee_transaction.objects
                        .filter(student_id=student_id, student_fee_id=student_fee_id)
                        .annotate(
                            month=F('payment_date__month'),
                            year=F('payment_date__year')
                        )
                    )

                    
                    paid_months = {(t.year, t.month) for t in transactions}

                    data = []
                    
                    for year, month in months:
                        if (year, month) not in paid_months:
                            month_has_passed = (year < current_date.year) or (year == current_date.year and month < current_date.month)
                            data.append({
                                'year': year,
                                'month': month,
                                'status': False,
                                'fine': 50.0 if month_has_passed else None,
                                'total': float(fee.amount)+50 if month_has_passed else fee.amount
                            })
                    
                    if len(data) == 0:
                        data = 'Not exist'
                except Exception:
                    pass
            return render(request,'student/fee_payment.html',{'data':data,'fee':fee,'sf_id':request.GET['sf_id']})
        else:
            obj = Student_register.objects.get(sr_id=request.session['student'])
            data = Student_fee.objects.filter(educational_level=obj.standard.educational_level).select_related('educational_level')
            ay = Academic_year.objects.all()
            return render(request,'student/fee_list.html',{'data':data,'ay':ay})
    else:
        return redirect('/home/')
    
def payment(request):
    if 'student' in request.session:
        if request.method == 'POST':
            ay=Academic_year.objects.get(current_ay=True)
            parsed_date = datetime.strptime(request.POST['dt'], "%Y-%m-%d")
            formatted_date = parsed_date.strftime("%Y-%m-%d")

            ob = Student_fee_transaction()
            ob.student_id = request.session['student']
            ob.academic_year = ay
            ob.student_fee_id = request.POST['sf_id']
            ob.total_amount = request.POST['amount']
            
            ob.payment_date = formatted_date
            ob.created_at=date.today()
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/student_fee/')
        else:
            current_date = date.today()
            dt = request.GET['ye']+'-'+request.GET['mo']+'-'+'01'
            t = date(int(request.GET['ye']), int(request.GET['mo']), 1)
            sf = Student_fee.objects.get(sf_id=request.GET['sf_id'])
            total = 0
            
            if (t.year < current_date.year) or (t.year == current_date.year and t.month < current_date.month):
                total = float(sf.amount)+50
            else:
                total = sf.amount
            return render(request,'student/payment.html',{'dt':dt,'sf':sf,'total':total})
    else:
        return redirect('/home/')



def edit_student_fee(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ob = Student_fee.objects.get(sf_id=request.POST['sf_id'])
            ob.account_category = request.POST['account_category']
            ob.educational_level_id = request.POST['educational_level_id']
            ob.fee_type = request.POST['fee_type']
            ob.amount = request.POST['amount']
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/student_fee/')
        else:
            data = Student_fee.objects.get(sf_id=request.GET['sf_id'])
            edl = Educational_level.objects.all()
            return render(request,'accountant/edit_student_fee.html',{'data':data,'edl':edl})
    else:
        return redirect('/home/')
    
def status_student_fee(request):
    if 'accountant' in request.session:
        data = Student_fee.objects.get(sf_id=request.GET['sf_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/student_fee/')
    else:
        return redirect('/home/')
    
def student_fee_transactions(request):
    data = Student_fee_transaction.objects.select_related('academic_year','student_fee','student').order_by('-sft_id')
    ay = Academic_year.objects.filter(status=True) 
    std = Standard.objects.select_related('educational_level')
    if 'master' in request.session:
        return render(request,'master/student_fee_transactions.html',{'data':data,'std':std,'ay':ay})
    if 'accountant' in request.session:
        return render(request,'accountant/student_fee_transactions.html',{'data':data,'std':std,'ay':ay})
    if 'student' in request.session:
        data = Student_fee_transaction.objects.filter(student_id=request.session['student']).select_related('academic_year','student_fee','student')
        return render(request,'student/student_fee_transactions.html',{'data':data})
    else:
        return redirect('/home/')

def staff_salary(request):
    if 'accountant' in request.session:
        current_date = date.today()
        current_year = current_date.year
        j = date(current_year, 6, 1)
        year_value = current_year if current_date >= j else current_year + 1

        ex = Academic_year.objects.filter(current_ay=True).exists()
        ay = None
        json_data = '{}'
        if ex:
            try:
                ay = Academic_year.objects.get(academic_year__startswith=year_value, current_ay=True)
                json_data = json.dumps(ay.academic_year) 
            except Exception:
                pass 

        return render(request, 'accountant/staff_salary.html', {'ay': ay, 'json_data': json_data})
    else:
        return redirect('/home/')

    
def search_staff_salary(request):
    chdate = request.GET['chdate']
    year, month = chdate.split('-')
    str1 = ''
    data = Staff_register.objects.filter(~Q(salary_transaction__salary_date__year=year,salary_transaction__salary_date__month=month))
    if data:
        str1+=f'''<div class="card">
                <h5 class="card-header">Staff list</h5>
                <div class="card-body">
                    <table class="table table-bordered">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Image</th>
                            <th>Name</th>
                            <th>Contact details</th>
                            <th>Designation</th>
                            <th>Salary month</th>
                            <th>#</th>
                        </tr>
                          </thead>
                          <tbody>'''
        c=0
        for i in data:
            c+=1
            str1+=f'''
                <tr>
                    <td>{c}</td>
                    <td><img src="{i.image}" class="rounded" style="height: 60px; width:60px;" alt=""></td>
                    <td>{i.name}</td>
                    <td>
                        Email : {i.login.username} <br>
                        Contact number : {i.contact_number} 
                    </td>
                    <td>{i.designation.designation_name}</td>
                    <td>{chdate}</td>
                    <td>
                        <a href="/salary_transaction?staff_id={ i.sr_id }&chdate={chdate}" class="btn btn-xs btn-info">Salary</a>
                    </td>
                </tr>
                    '''
        str1+='</tbody></table></div></div>'
    else:
        str1 += '<div class="col-lg-12" data-aos="fade-up" data-aos-delay="100">Not found any pending salary</div>'
    return HttpResponse(str1)

def salary_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            ay = Academic_year.objects.get(current_ay=True)
            obj = Salary_transaction()
            obj.staff_id = request.POST['staff_id']
            obj.academic_year = ay
            obj.salary_table_id = request.POST['salary_table_id']
            obj.deductions = request.POST['deductions']
            obj.agp_amount = request.POST['agp']
            obj.da_amount = request.POST['da']
            obj.hra_amount = request.POST['hra']
            obj.ta_amount = request.POST['ta']
            if request.POST['bonus'] !='':
                obj.bonus = request.POST['bonus']
            
            obj.salary_date = request.POST['salary_date']
            obj.basic_pay = request.POST['basic_pay']
            obj.save()
            messages.success(request, 'Salary added successfully.')
            return redirect('/staff_salary/')
        elif 'staff_id' in request.GET:
            chdate = request.GET['chdate']
            year, month = chdate.split('-')
            leave_excess = Staff_leave.objects.filter(
                    staff_id=request.GET['staff_id'], 
                    status="Approved", 
                    start_date__month=month,
                    start_date__year=year,
                ) .values('leave_type__leave_type').annotate(
                    total_days=Sum('no_of_days'),  
                    allowed_days=F('leave_type__days'),  
                    excess_days=Case(
                        When(total_days__gt=F('leave_type__days'), 
                            then=F('total_days') - F('leave_type__days')),
                        default=Value(0)  
                    )
                ).filter(excess_days__gt=0)  


            total_excess_days = leave_excess.aggregate(total_excess=Sum('excess_days'))['total_excess']
            data = Staff_register.objects.get(sr_id=request.GET['staff_id'])
            st = get_object_or_404(
                Salary_table.objects.annotate(
                    da_amount=(F('basic_pay')*(F('da')/100)),
                    ta_amount=(F('basic_pay')*(F('ta')/100)),
                    hra_amount=(F('basic_pay')*(F('hra')/100)),
                    agp_amount=(F('basic_pay')*(F('agp')/100)),
                ),
                designation_id=data.designation_id
            )
            
            deduction = 0
            if total_excess_days: 
                deduction = total_excess_days * int(st.basic_pay)/30
            
            return render(request,'accountant/salary_transaction.html',{'le':leave_excess,'data':data,'ted':total_excess_days,'dd':deduction,'st':st,'chdate':chdate})
        else:
            return redirect('/staff_salary/')
    else:
        return redirect('/home/')
    
def school_finance_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            obj = School_finance_transaction()
            obj.academic_year_id = request.POST['academic_year_id']
            obj.school_finance_id = request.POST['school_finance_id']
            obj.description = request.POST['description']
            obj.total_amount = request.POST['total_amount']
            obj.entry_date = date.today()
            obj.save()
            messages.success(request, 'Added successfully.')
            return redirect('/school_finance_transaction/')
        else:
            ay = Academic_year.objects.filter(status=True)
            data = School_finance.objects.filter(status=True,account_category=request.GET.get('actype'))       
            return render(request,'accountant/school_finance_transaction.html',{'data':data,'ay':ay})
    else:
        return redirect('/home/')
    
def edit_finance_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            obj = School_finance_transaction.objects.get(sft_id=request.POST.get('sft_id')) 
            obj.academic_year_id = request.POST['academic_year_id']
            obj.school_finance_id = request.POST['school_finance_id']
            obj.description = request.POST['description']
            obj.total_amount = request.POST['total_amount']
            obj.approval_status = None
            obj.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/school_finance_transaction/')
        else:
            ay = Academic_year.objects.filter(status=True)
            data = School_finance_transaction.objects.get(sft_id=request.GET.get('sft_id')) 
            sf = School_finance.objects.filter(status=True)    
            return render(request,'accountant/edit_finance_transaction.html',{'data':data,'ay':ay,'sf':sf})
    else:
        return redirect('/home/')

def new_salary_transactions(request):
    data = Salary_transaction.objects.filter(Q(approval_status=None)|Q(approval_status='Denied')).select_related('staff','academic_year','salary_table')         
    if 'accountant' in request.session:
        return render(request,'accountant/salary_transactions_list.html',{'data':data})
    elif 'master' in request.session:
        return render(request,'master/salary_transactions_list.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_salary_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            obj = Salary_transaction.objects.get(st_id=request.POST.get('st_id'))
            obj.deductions = request.POST['deductions']
            obj.agp_amount = request.POST['agp']
            obj.da_amount = request.POST['da']
            obj.hra_amount = request.POST['hra']
            obj.ta_amount = request.POST['ta']
            if request.POST['bonus'] !='':
                obj.bonus = request.POST['bonus']
            
            obj.basic_pay = request.POST['basic_pay']
            obj.approval_status = None
            obj.save()
            messages.success(request, 'Updated added successfully.')
            return redirect('/staff_salary/')
        elif 'st_id' in request.GET:
            data = Salary_transaction.objects.get(st_id=request.GET.get('st_id'))
            return render(request,'accountant/edit_salary_transaction.html',{'data':data})
    else:
        return redirect('/home/')


def salary_details(request):
    if 'st_id' in request.GET:
        data = (
        Salary_transaction.objects
                .annotate(total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions'))
                .get(st_id=request.GET['st_id'])
            )      
        if 'accountant' in request.session:
            return render(request,'accountant/salary_details.html',{'data':data})
        elif 'master' in request.session:
            return render(request,'master/salary_details.html',{'data':data})
        elif 'office_staff' in request.session:
            return render(request,'office_staff/salary_details.html',{'data':data})
        elif 'faculty' in request.session:
            return render(request,'faculty/salary_details.html',{'data':data})
        else:
            return redirect('/home/')
    else:
        return redirect('/salary_transactions_list/')

def salary_transactions_history(request):
    data = Salary_transaction.objects.filter(approval_status='Approved').annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions')             
    ).select_related('staff','academic_year','salary_table')  
    ay = Academic_year.objects.filter(status=True) 
    staff = Staff_register.objects.select_related('designation','login')      
    if 'accountant' in request.session:
        return render(request,'accountant/salary_transactions_history.html',{'data':data,'ay':ay,'staff':staff})
    elif 'master' in request.session:
        return render(request,'master/salary_transactions_history.html',{'data':data,'ay':ay,'staff':staff})
    elif 'faculty' in request.session:
        data = Salary_transaction.objects.filter(approval_status='Approved',staff_id=request.session['staff_id']).annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions')             
            ).select_related('staff','academic_year','salary_table')
        return render(request,'faculty/salary_transactions_history.html',{'data':data})
    elif 'office_staff' in request.session:
        data = Salary_transaction.objects.filter(approval_status='Approved',staff_id=request.session['staff_id']).annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions')             
            ).select_related('staff','academic_year','salary_table')
        return render(request,'office_staff/salary_transactions_history.html',{'data':data})
    else:
        return redirect('/home/')

def salary_transactions_accountant(request):
    if 'accountant' in request.session:
        data = Salary_transaction.objects.filter(approval_status='Approved',staff_id=request.session['staff_id']).annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions')             
            ).select_related('staff','academic_year','salary_table')
        return render(request,'accountant/salary.html',{'data':data})
    else:
        return redirect('/home/')

def salary_transactions_status(request):
    if 'master' in request.session:
        if 'st_id' in request.GET:
            obj = Salary_transaction.objects.get(st_id=request.GET['st_id'])
            obj.approval_status = request.GET['status']
            obj.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('/salary_transactions_history/')
        else:
            return redirect('/new_salary_transactions/')
    else:
        return redirect('/home/')
    
def new_school_finance_transactions(request):
    data = School_finance_transaction.objects.filter(Q(approval_status=None)|Q(approval_status='Denied')).select_related('academic_year','school_finance')         
    if 'accountant' in request.session:
        return render(request,'accountant/school_finance_transaction_list.html',{'data':data})
    elif 'master' in request.session:
        return render(request,'master/school_finance_transaction_list.html',{'data':data})
    else:
        return redirect('/home/')

def school_finance_transaction_status(request):
    if 'master' in request.session:
        if 'sft_id' in request.GET:
            obj = School_finance_transaction.objects.get(sft_id=request.GET['sft_id'])
            obj.approval_status = request.GET['status']
            obj.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('/school_finance_transactions_history/')
        else:
            return redirect('/new_school_finance_transactions/')
    else:
        return redirect('/home/')

def school_finance_transactions_history(request):
    ay = Academic_year.objects.filter(status=True) 
    data = School_finance_transaction.objects.filter(approval_status='Approved').select_related('academic_year','school_finance')         
    if 'accountant' in request.session:
        return render(request,'accountant/school_finance_transaction_history.html',{'data':data,'ay':ay})
    elif 'master' in request.session:
        return render(request,'master/school_finance_transaction_history.html',{'data':data,'ay':ay})
    else:
        return redirect('/home/')
    

def search_salary(request):
    str1 = ''
    pdfurlpath = "/salary_pdf?s="
    if request.GET['ay_id'] == '':
        ay_query = Q()
    else:
        ay_query = Q(academic_year_id=request.GET['ay_id'])
        pdfurlpath += "&ay_id="+request.GET['ay_id']

    if request.GET['staff_id'] == '':
        staff_query = Q()
    else:
        staff_query = Q(staff_id=request.GET['staff_id'])
        pdfurlpath += "&staff_id="+request.GET['staff_id']

    if request.GET['my'] == '':
        my_query = Q()
    else:
        my = request.GET['my']
       
        my_query = Q(salary_date__month=my)
        pdfurlpath += "&mo="+my

    data = Salary_transaction.objects.filter(ay_query,staff_query,my_query,approval_status='Approved').annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions')             
        ).select_related('staff','academic_year','salary_table') 
    if data:
        c = 0
        for i in data:
            c+=1
            str1+=f'''
            <tr>
                <td>{c}</td>
                <td><img src="{i.staff.image}" class="rounded" style="height: 60px; width:60px;" alt=""></td>
                <td>
                    {i.staff.name} <br>
                    Email : {i.staff.login.username} <br>
                    Contact number : {i.staff.contact_number}
                </td>
                <td>{ i.academic_year.academic_year }</td>
                <td>{i.total_salary}</td>
                <td>{ i.salary_date } </td>
                <td>'''
            if i.approval_status == None:
                str1+='<div class="badge badge-warning">Pending</div>'
            elif i.approval_status == 'Approved':
                str1+=f'<div class="badge badge-success">{i.approval_status}</div>'
            else:
                str1+=f'<div class="badge badge-danger">{i.approval_status}</div>'
                       
            str1+=f'''</td>
            <td>
                <a href="/salary_details?st_id={ i.st_id }" class="btn btn-xs btn-primary">Salary details</a>
            </td>
            </tr>
                    '''
        str1+=f'<tr><td colspan="7"><a href="{pdfurlpath}" class="text-secondary">Download PDF</a><td><tr>'
    else:
        str1+= '<tr><td colspan="8"><b class="font-monospace text-danger">Not found salary details</b></td></tr>'
    return HttpResponse(str1)

def search_school_finance(request):
    str1 = ''
    pdfurlpath = "/school_finance_pdf?s="
    if request.GET['ay_id'] == '':
        ay_query = Q()
    else:
        ay_query = Q(academic_year_id=request.GET['ay_id'])
        pdfurlpath += "&ay_id="+request.GET['ay_id']

    if request.GET['my'] == '':
        my_query = Q()
    else:
        my = request.GET['my']
        my_query = Q(entry_date__month=my)
      
        pdfurlpath += "&mo="+my
    
    if request.GET['ac'] == '':
        ac_query = Q()
    else:
        ac_query = Q(school_finance__account_category=request.GET['ac'])
        pdfurlpath += "&ac="+request.GET['ac']
    print(ac_query)
    data = School_finance_transaction.objects.filter(ay_query,my_query,ac_query,approval_status='Approved').select_related('academic_year','school_finance')       
   
    if data:
        c = 0
        for i in data:
            c+=1
            str1+=f'''
            <tr>
                <td>{c}</td>
                <td>{ i.academic_year.academic_year }</td>
                <td>{i.school_finance.finance_type}</td>
                <td>{i.school_finance.account_category}</td>
                <td>{ i.total_amount } </td>
                <td>{ i.entry_date } </td>
                <td>{ i.description } </td><td>'''
            if i.approval_status == 'Approved':
                str1+=f'<div class="badge badge-success">{i.approval_status}</div>'
            else:
                str1+=f'<div class="badge badge-danger">{i.approval_status}</div>'
                       
            str1+=f'''</td>
            
            </tr>
                    '''
        str1+=f'<tr><td colspan="6"><a href="{pdfurlpath}" class="text-secondary">Download PDF</a><td><tr>'
    else:
        str1+= '<tr><td colspan="7"><b class="font-monospace text-danger">Not found any list</b></td></tr>'
    return HttpResponse(str1)

def search_student_fee(request):
    str1 = ''
    pdfurlpath = "/student_fee_pdf?s="
    if request.GET['ay_id'] == '':
        ay_query = Q()
    else:
        ay_query = Q(academic_year_id=request.GET['ay_id'])
        pdfurlpath += "&ay_id="+request.GET['ay_id']

    if request.GET['s_id'] == '':
        standard_query = Q()
    else:
        standard_query = Q(student__standard_id=request.GET['s_id'])
        pdfurlpath += "&s_id="+request.GET['s_id']

    if request.GET['my'] == '':
        my_query = Q()
    else:
        my = request.GET['my']
        my_query = Q(payment_date__month=my)
        pdfurlpath += "&mo="+my

    data = Student_fee_transaction.objects.filter(ay_query,standard_query,my_query).select_related('academic_year','student_fee','student') 
    if data:
        c = 0
        for i in data:
            c+=1
            str1+=f'''<tr>
                <td>{c}</td>
                <td><img src="{i.student.image}" class="rounded" style="height: 60px; width:60px;" alt=""></td>
                <td>
                    {i.student.name} <br>
                    Contact number : {i.student.contact_number} <br>
                    Education level : { i.student.standard.educational_level.level } <br>
                    Standard : { i.student.standard.standard }
                </td>
                <td>{ i.academic_year.academic_year }</td>
                <td>{i.student_fee.fee_type} : { i.payment_date} </td>
                <td>{ i.created_at } </td>
                <td>{ i.total_amount }</td></tr> '''
        str1+=f'<tr><td colspan="6"><a href="{pdfurlpath}" class="text-secondary">Download PDF</a><td><tr>'
    else:
        str1+= '<tr><td colspan="8"><b class="font-monospace text-danger">Not found salary details</b></td></tr>'
    return HttpResponse(str1)


def salary_pdf(request):
    ay_query = Q(academic_year_id=request.GET.get('ay_id')) if 'ay_id' in request.GET else Q()
    staff_query = Q(staff_id=request.GET.get('staff_id')) if 'staff_id' in request.GET else Q()
    my_query = Q(salary_date__month=request.GET.get('mo')) if 'mo' in request.GET else Q()

    data = Salary_transaction.objects.filter(ay_query & staff_query & my_query,approval_status='Approved').annotate(
        total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),
        payable=F('total_salary') - F('deductions')
    ).select_related('staff', 'academic_year', 'salary_table')

    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="salary_pdf.pdf"'

    html = render_to_string('pdf_template.html', {'data': data,'heading':'Staff salary details'})

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response

def school_finance_pdf(request):
    ay_query = Q(academic_year_id=request.GET.get('ay_id')) if 'ay_id' in request.GET else Q()
    my_query = Q(entry_date__month=request.GET.get('mo')) if 'mo' in request.GET else Q()
    ac_query = Q(school_finance__account_category=request.GET['ac']) if 'ac' in request.GET else Q()

    data = School_finance_transaction.objects.filter(ay_query, my_query,ac_query,approval_status='Approved').select_related('academic_year', 'school_finance')  

    
    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="school_finance_pdf.pdf"'

    html = render_to_string('pdf_template.html', {'data': data,'heading':'School finance details'})

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response

def student_fee_pdf(request):
    ay_query = Q(academic_year_id=request.GET.get('ay_id')) if 'ay_id' in request.GET else Q()
    standard_query = Q(student__standard_id=request.GET.get('s_id')) if 's_id' in request.GET else Q()
    date_query = Q(payment_date__month=request.GET.get('mo')) if 'mo' in request.GET else Q()

    data = Student_fee_transaction.objects.filter(ay_query & standard_query & date_query).select_related('academic_year', 'student_fee', 'student') 

    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="student_fee_pdf.pdf"'

    html = render_to_string('pdf_template.html', {'data': data,'heading':'Student fee details'})

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response

def fee_pdf(request):
    
    data = Student_fee_transaction.objects.get(sft_id=request.GET.get('sft_id')) 

    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="student_fee_pdf.pdf"'

    html = render_to_string('student_fee_pdf.html', {'data': data})

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response


def student_fee_dues(request):
    if 'dt' in request.GET:
        chdate = request.GET['dt']
        year, month = chdate.split('-')
        
        standard_id = request.GET.get('s_id')

        standard = Standard.objects.get(pk=standard_id)
        educational_level = standard.educational_level

        fees_for_level = Student_fee.objects.filter(educational_level=educational_level)

        students = Student_register.objects.filter(standard=standard)

        student_data = []  

        for student in students:
            paid_fee_ids = Student_fee_transaction.objects.filter(
                student=student,
                payment_date__month=month,
                payment_date__year=year
            ).values_list('student_fee_id', flat=True)

            unpaid_fees = fees_for_level.exclude(sf_id__in=paid_fee_ids)

            student_data.append({
                'student': student,
                'unpaid_fees': unpaid_fees
            })
        
        str1 = ''
        if student_data:
            str1 += '''
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Image</th>
                            <th>Name</th>
                            <th>Contact details</th>
                            <th>Standard</th>
                            <th>Unpaid Fees</th>
                        </tr>
                    </thead>
                    <tbody>
                '''
            c = 0
            for i in student_data:
                student = i['student']  # Access the 'student' key from the dictionary
                unpaid_fees = i['unpaid_fees']  # Access the 'unpaid_fees' key from the dictionary

                c += 1
                str1 += f'''
                    <tr>
                        <td>{c}</td>
                        <td><img src="{student.image}" alt="Student Image" width="50" /></td>
                        <td>{student.name}</td>
                        <td>
                            Email: {student.email}<br>
                            Contact: {student.contact_number}<br>
                            Address: {student.address}
                        </td>
                        <td>{student.standard.standard}</td>
                        <td>
                            <ul>
                '''
                for fee in unpaid_fees:
                    str1 += f'<li>{fee.fee_type} - ₹{fee.amount}</li>'
                
                str1 += '''
                            </ul>
                        </td>
                    </tr>
                '''
            
            str1 += '</tbody></table>'
        else:
            str1 += '<h3 class="font-monospace text-danger">Not found any dues</h3>'

        return HttpResponse(str1)

    else:
        data = Standard.objects.select_related('educational_level')
        if 'accountant' in request.session:
            template_name = 'accountant/student_fee_dues.html'
        elif 'master' in request.session:
            template_name = 'master/student_fee_dues.html'
        else:
            return redirect('/home/')

        return render(request, template_name, {'std':data})


def salary_slip(request):
    data = (
        Salary_transaction.objects
                .annotate(total_salary=F('basic_pay') + F('bonus') + F('da_amount') + F('hra_amount') + F('ta_amount') + F('agp_amount'),payable=F('total_salary')-F('deductions'))
                .get(st_id=request.GET['st_id'])
            ) 
    id = request.GET['st_id']
    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="slip_{id}.pdf"'

    html = render_to_string('salary_slip.html', {'data': data})

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response
    # return render(request,'salary_slip.html',{'data':data})

def school_transactions(request):
    ay = Academic_year.objects.filter(status=True) 
    if 'master' in request.session:
        return render(request,'master/school_transactions.html',{'ay':ay})
    if 'accountant' in request.session:
        return render(request,'accountant/school_transactions.html',{'ay':ay})

def school_transactions_search(request):
    pdfurlpath = "/school_transactions_pdf?s="
    if 'ay_id' in request.GET:
        ay_query = Q(academic_year_id=request.GET.get('ay_id'))
    else:
        ay_query = Q()

    if request.GET.get('sm')=='' and request.GET.get('em')=='':
        student_fee_query = Q()
        staff_salary_query = Q()
        sft_query = Q()
        pdfurlpath += "&ay_id="+request.GET['ay_id']
    elif request.GET.get('em')=='' and request.GET.get('sm')!='':
        student_fee_query = Q(payment_date__month=request.GET.get('sm'))
        staff_salary_query = Q(salary_date__month=request.GET.get('sm'))
        sft_query = Q(entry_date__month=request.GET.get('sm'))
        pdfurlpath += "&ay_id="+request.GET['ay_id']+"&sm="+request.GET.get('sm')
    elif request.GET.get('em')!='' and request.GET.get('sm')!='':
        student_fee_query = Q(payment_date__month__range=(request.GET.get('sm'),request.GET.get('em')))
        staff_salary_query = Q(salary_date__month__range=(request.GET.get('sm'),request.GET.get('em')))
        sft_query = Q(entry_date__month__range=(request.GET.get('sm'),request.GET.get('em')))
        pdfurlpath += "&ay_id="+request.GET['ay_id']+"&sm="+request.GET.get('sm')+"&em="+request.GET.get('em')
    else:
        pdfurlpath += "&ay_id="+request.GET['ay_id']
        student_fee_query = Q()
        staff_salary_query = Q()
        sft_query = Q()

    
    student = Student_fee_transaction.objects.filter(ay_query,student_fee_query).aggregate(fee=Sum('total_amount'))
    staff = Salary_transaction.objects.filter(ay_query,staff_salary_query).aggregate(salary=Sum('basic_pay')+Sum('agp_amount')+Sum('ta_amount')+Sum('hra_amount')+Sum('da_amount')+Sum('bonus')-Sum('deductions'))
    school_income = School_finance_transaction.objects.filter(ay_query,sft_query,school_finance__account_category='Income').aggregate(sf_income=Sum('total_amount'))
    school_expense = School_finance_transaction.objects.filter(ay_query,sft_query,school_finance__account_category='Expense').aggregate(sf_expense=Sum('total_amount'))

    if student['fee'] == None:
        student['fee'] = 0
    if staff['salary'] == None:
        staff['salary'] = 0 
    if school_income['sf_income'] == None:
        school_income['sf_income'] = 0
    if school_expense['sf_expense'] == None:
        school_expense['sf_expense'] = 0

    total_income = float(student['fee']) + float(school_income['sf_income'])
    total_expense = staff['salary'] + school_expense['sf_expense']

    str1 = f'''
            <div class="card w-100">
                <h5 class="card-header">School Transactions</h5>
                <div class="card-body">
                    <div class="mb-2"><a href="{pdfurlpath}" class="text-secondary float-right">Download PDF <i class="fa fa-file-pdf text-danger"></i></a><td></div>
                    <table class="table table-bordered mb-4">
                        <thead>
                        <tr><th colspan="3">Incomes :</th></tr>
                        <tr>
                            <th>#</th>
                            <th>Finance Type</th>
                            <th>Total</th>
                        </tr>
                          </thead>
                          <tbody>
                            <tr>
                                <td>1</td>
                                <td>Student fee</td>
                                <td>{ student['fee']}</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>School Finance Income</td>
                                <td>{ school_income['sf_income'] }</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered mb-4">
                        <thead>
                        <tr><th colspan="3">Expense :</th></tr>
                        <tr>
                            <th>#</th>
                            <th>Finance Type</th>
                            <th>Total</th>
                        </tr>
                          </thead>
                          <tbody>
                            <tr>
                                <td>1</td>
                                <td>Staff salary</td>
                                <td>{ staff['salary'] }</td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>School Finance expense</td>
                                <td>{ school_expense['sf_expense'] }</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered">
                        <thead>
                            <tr><th colspan="2">Total :</th></tr>
                            <tr>
                                <th>Total Income</th>
                                <td>{ total_income }</td>
                            </tr>
                            <tr>
                                <th>Total Expense</th>
                                <th>{ total_expense }</th>
                            </tr>
                        </thead>
                    </table>
                    </div>
            </div>
        '''
    return HttpResponse(str1)

def school_transactions_pdf(request):
    if 'ay_id' in request.GET:
        ay_query = Q(academic_year_id=request.GET.get('ay_id'))
        student_fee_query = Q()
        staff_salary_query = Q()
        sft_query = Q()
    else:
        ay_query = Q()
        student_fee_query = Q()
        staff_salary_query = Q()
        sft_query = Q()

    if 'sm' in request.GET:
        student_fee_query = Q(payment_date__month=request.GET.get('sm'))
        staff_salary_query = Q(salary_date__month=request.GET.get('sm'))
        sft_query = Q(entry_date__month=request.GET.get('sm'))

    if 'sm' and 'em' in request.GET:
        student_fee_query = Q(payment_date__month__range=(request.GET.get('sm'),request.GET.get('em')))
        staff_salary_query = Q(salary_date__month__range=(request.GET.get('sm'),request.GET.get('em')))
        sft_query = Q(entry_date__month__range=(request.GET.get('sm'),request.GET.get('em')))

    student = Student_fee_transaction.objects.filter(ay_query,student_fee_query).aggregate(fee=Sum('total_amount'))
    staff = Salary_transaction.objects.filter(ay_query,staff_salary_query).aggregate(salary=Sum('basic_pay')+Sum('agp_amount')+Sum('ta_amount')+Sum('hra_amount')+Sum('da_amount')+Sum('bonus')-Sum('deductions'))
    school_income = School_finance_transaction.objects.filter(ay_query,sft_query,school_finance__account_category='Income').aggregate(sf_income=Sum('total_amount'))
    school_expense = School_finance_transaction.objects.filter(ay_query,sft_query,school_finance__account_category='Expense').aggregate(sf_expense=Sum('total_amount'))

    if student['fee'] == None:
        student['fee'] = 0
    if staff['salary'] == None:
        staff['salary'] = 0 
    if school_income['sf_income'] == None:
        school_income['sf_income'] = 0
    if school_expense['sf_expense'] == None:
        school_expense['sf_expense'] = 0

    total_income = float(student['fee']) + float(school_income['sf_income'])
    total_expense = staff['salary'] + school_expense['sf_expense']

    response = HttpResponse (content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="school_transactions_pdf.pdf"'
    context = {
        'total_income': total_income,'total_expense': total_expense,
        'student': student,'staff': staff,
        'school_income': school_income,'school_expense': school_expense
    }
    html = render_to_string('school_transactions_pdf.html',context)

    pisa_status = pisa.CreatePDF(html, dest=response) 

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')   
    return response


def check_academic_year_exist(request):
    academic_year = request.GET.get('academic_year', None)
    exists = Academic_year.objects.filter(academic_year__startswith=academic_year).exists()
    return JsonResponse({'exists': exists})

def check_value_exist2(request):
    chval = request.GET.get('chval', None)
    fil = request.GET.get('fil', None)
    tbl = apps.get_model('schoolapp',request.GET.get('tbl'))
    exists = tbl.objects.filter(**{fil:chval}).exists()
    return JsonResponse({'exists': exists})

def check_value_exist(request):
    chval = request.GET.get('chval', None)  
    fil = request.GET.get('fil', None)     
    tbl = apps.get_model('schoolapp', request.GET.get('tbl'))  

    filter_param = f"{fil}__iregex"
    exists = tbl.objects.filter(**{filter_param: chval}).exists()

    return JsonResponse({'exists': exists})

def check_leave_exist(request):
    start_date = datetime.strptime(request.GET.get('start_date', None), '%Y-%m-%d').date()
    end_date= datetime.strptime(request.GET.get('end_date', None), '%Y-%m-%d').date()
    exists = Staff_leave.objects.filter(
    Q(staff_id=request.session['staff_id']) &
    (
        Q(start_date__lte=end_date, end_date__gte=start_date)  
    )
    ).exists()
    return JsonResponse({'exists': exists})
 
def check_student_fee_exist(request):
    exists = Student_fee.objects.filter(
        educational_level_id=request.GET.get('educational_level_id'),
        fee_type=request.GET.get('fee_type')
        ).exists()
    return JsonResponse({'exists': exists})



def sign_out(request):
    logout(request)
    request.session.delete()
    return redirect('/home/')

def check_username(request):
    username = request.GET.get("username")
    exists =  Login.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def check_email(request):
    email = request.GET.get("email")
    exists =  Login.objects.filter(username=email).exists()
    return JsonResponse({'exists': exists})

def master_reg(request):
    if request.method == 'POST': 
        ob = Login()
        ob.username = request.POST['username']
        ob.password =  request.POST['password']
        ob.user_type = 'admin'
        ob.save()
        return redirect('/login/')
    else:
        return render(request,'master_reg.html')