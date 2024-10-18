from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import date,datetime,timedelta
from django.db.models import Q,Min,Count,Sum, F, Case, When, Value
from django.middleware.csrf import get_token
from django.apps import apps
from email.message import EmailMessage
from django.conf import settings
import ssl
import smtplib
import random
import string
 
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
            if data.status == None:
                request.session['login_id'] = data.login_id
                return redirect('/home/')
            else:
                messages.success(request,'Admin Approval required for login')
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
            messages.success(request, 'Updated successfully')
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
            email_sender="nirmalbehanan03@gmail.com"    
            email_password="EMAIL_PASSWORD"
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
        dt = Designation.objects.all()
        return render(request,'master/staff_register.html',{'designation':dt})


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
    if 'master' in request.session:
        if request.method == 'POST':
            ob = School_finance()
            ob.account_category = request.POST['account_category']
            ob.finance_type = request.POST['finance_type']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/school_finance/')
        else:
            data = School_finance.objects.all()
            return render(request,'master/school_finance.html',{'data':data})
    else:
        return redirect('/home/')
    
def edit_school_finance(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = School_finance.objects.get(sf_id=request.POST['sf_id'])
            ob.account_category = request.POST['account_category']
            ob.finance_type = request.POST['finance_type']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/school_finance/')
        else:
            data = School_finance.objects.get(sf_id=request.GET['sf_id'])
            return render(request,'master/edit_school_finance.html',{'data':data})
    else:
        return redirect('/home/')
    
def status_school_finance(request):
    if 'master' in request.session:
        data = School_finance.objects.get(sf_id=request.GET['sf_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/school_finance/')
    else:
        return redirect('/home/')

def salary_table(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Salary_table()
            ob.account_category = request.POST['account_category']
            ob.designation_id = request.POST['designation_id']
            ob.basic_pay = request.POST['basic_pay']
            ob.save()
            messages.success(request, 'Added successfully.')
            return redirect('/salary_table/')
        else:
            data = Salary_table.objects.select_related('designation')
            des = Designation.objects.all()
            return render(request,'master/salary_table.html',{'data':data,'des':des})
    else:
        return redirect('/home/')

def edit_salary_table(request):
    if 'master' in request.session:
        if request.method == 'POST':
            ob = Salary_table.objects.get(st_id=request.POST['st_id'])
            ob.account_category = request.POST['account_category']
            ob.designation_id = request.POST['designation_id']
            ob.basic_pay = request.POST['basic_pay']
            ob.save()
            messages.success(request, 'Updated successfully.')
            return redirect('/salary_table/')
        else:
            data = Salary_table.objects.get(st_id=request.GET['st_id'])
            des = Designation.objects.all()
            return render(request,'master/edit_salary_table.html',{'data':data,'des':des})
    else:
        return redirect('/home/')
    
def status_salary_table(request):
    if 'master' in request.session:
        data = Salary_table.objects.get(st_id=request.GET['st_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/salary_table/')
    else:
        return redirect('/home/')
    
def student_fee(request):
    if 'master' in request.session:
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
            return render(request,'master/student_fee.html',{'data':data,'edl':edl})
    else:
        return redirect('/home/')
    
def edit_student_fee(request):
    if 'master' in request.session:
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
            return render(request,'master/edit_student_fee.html',{'data':data,'edl':edl})
    else:
        return redirect('/home/')
    
def status_student_fee(request):
    if 'master' in request.session:
        data = Student_fee.objects.get(sf_id=request.GET['sf_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/student_fee/')
    else:
        return redirect('/home/')
    
def staff_salary(request):
    if 'accountant' in request.session:
        return render(request,'accountant/staff_salary.html')
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
        str1 += '<div class="col-lg-12" data-aos="fade-up" data-aos-delay="100">Not found any book</div>'
    return HttpResponse(str1)

def salary_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            obj = Salary_transaction()
            obj.staff_id = request.POST['staff_id']
            obj.academic_year_id = request.POST['academic_year_id']
            obj.salary_table_id = request.POST['salary_table_id']
            obj.deductions = request.POST['deductions']
            if request.POST['bonus'] !='':
                obj.bonus = request.POST['bonus']
            if request.POST['arrear'] !='':
                obj.arrear = request.POST.get('arrear',0)
            if request.POST['advance'] !='':
                obj.advance = request.POST.get('advance',0)
            if request.POST['agp'] !='':
                obj.agp = request.POST['agp']
            obj.salary_date = request.POST['salary_date']
            obj.basic_pay = request.POST['basic_pay']


            def getval(bp,val):
                return float(bp)*(float(val)/100)
            
            if request.POST['ta'] !='':
                obj.ta = getval(request.POST['basic_pay'],request.POST['ta'])
            
            if request.POST['da'] !='':
                obj.da = getval(request.POST['basic_pay'],request.POST['da'])

            if request.POST['hra'] !='':
                obj.hra = getval(request.POST['basic_pay'],request.POST['hra'])
            
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
            bp = Salary_table.objects.get(designation_id=data.designation_id)
            deduction = 0
            if total_excess_days: 
                deduction = total_excess_days * int(bp.basic_pay)/30
            ay = Academic_year.objects.all()
            return render(request,'accountant/salary_transaction.html',{'le':leave_excess,'data':data,'ted':total_excess_days,'dd':deduction,'bp':bp,'ay':ay,'chdate':chdate})
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
            messages.success(request, 'Salary added successfully.')
            return redirect('/school_finance_transaction/')
        else:
            ay = Academic_year.objects.all()
            data = School_finance.objects.all()          
            return render(request,'accountant/school_finance_transaction.html',{'data':data,'ay':ay})
    else:
        return redirect('/home/')

def new_salary_transactions(request):
    data = Salary_transaction.objects.filter(approval_status=None).select_related('staff','academic_year','salary_table')         
    if 'accountant' in request.session:
        return render(request,'accountant/salary_transactions_list.html',{'data':data})
    elif 'master' in request.session:
        return render(request,'master/salary_transactions_list.html',{'data':data})
    else:
        return redirect('/home/')
    
def salary_details(request):
    if 'st_id' in request.GET:
        data = (
        Salary_transaction.objects
                .annotate(total_salary=F('basic_pay') + F('bonus') + F('da') + F('hra') + F('ta') + F('agp'),payable=F('total_salary')-F('deductions'))
                .get(st_id=request.GET['st_id'])
            )      
        if 'accountant' in request.session:
            return render(request,'accountant/salary_details.html',{'data':data})
        elif 'master' in request.session:
            return render(request,'master/salary_details.html',{'data':data})
        else:
            return redirect('/home/')
    else:
        return redirect('/salary_transactions_list/')

def salary_transactions_history(request):
    data = Salary_transaction.objects.filter(~Q(approval_status=None)).select_related('staff','academic_year','salary_table')         
    if 'accountant' in request.session:
        return render(request,'accountant/salary_transactions_list.html',{'data':data})
    elif 'master' in request.session:
        return render(request,'master/salary_transactions_list.html',{'data':data})
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
    data = School_finance_transaction.objects.filter(approval_status=None).select_related('academic_year','school_finance')         
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
    data = School_finance_transaction.objects.filter(~Q(approval_status=None)).select_related('academic_year','school_finance')         
    if 'accountant' in request.session:
        return render(request,'accountant/school_finance_transaction_list.html',{'data':data})
    elif 'master' in request.session:
        return render(request,'master/school_finance_transaction_list.html',{'data':data})
    else:
        return redirect('/home/')
    


def check_academic_year_exist(request):
    academic_year = request.GET.get('academic_year', None)
    exists = Academic_year.objects.filter(academic_year__startswith=academic_year).exists()
    return JsonResponse({'exists': exists})

def check_value_exist(request):
    chval = request.GET.get('chval', None)
    fil = request.GET.get('fil', None)
    tbl = apps.get_model('schoolapp',request.GET.get('tbl'))
    exists = tbl.objects.filter(**{fil:chval}).exists()
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