from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import date, datetime, timedelta
import calendar
from django.utils import timezone
from django.db.models import Q,Min,Count,Sum, F, Case, When, Value, CharField, BooleanField,OuterRef,FloatField,Exists,Subquery,Prefetch,JSONField,IntegerField
from django.db.models.functions import Cast, Substr
from django.middleware.csrf import get_token
from django.apps import apps
from email.message import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import smtplib
import random
import string
import json
import razorpay
from django.conf import settings
from .blockchain import Blockchain
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
import os
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
import ssl

 
# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def home(request):
    # Check and update current academic year
    check_and_update_academic_year()
    
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
        return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            print("DEBUG: Login attempt for username:", username)
            data = Login.objects.get(username=username, password=password)
            
            if data.status == True:
                # Clear any existing session
                request.session.flush()
                
                # Set base session data
                request.session['login_id'] = data.login_id
                request.session['user_type'] = data.user_type
                
                # Set role-specific session data
                if data.user_type == 'admin':
                    request.session['master'] = data.login_id
                    print("DEBUG: Admin login successful, session:", dict(request.session))
                    return redirect('/master_home/')
                elif data.user_type == 'Accountant':
                    use = Staff_register.objects.get(login_id=data.login_id)
                    request.session['accountant'] = use.sr_id
                    request.session['staff_id'] = use.sr_id
                    print("DEBUG: Accountant login successful, session:", dict(request.session))
                    return redirect('/accountant_home/')
                elif data.user_type == 'Office staff':
                    use = Staff_register.objects.get(login_id=data.login_id)
                    request.session['office_staff'] = use.sr_id
                    request.session['staff_id'] = use.sr_id
                    return redirect('/office_staff_home/')
                elif data.user_type == 'Faculty':
                    use = Staff_register.objects.get(login_id=data.login_id)
                    request.session['faculty'] = use.sr_id
                    request.session['staff_id'] = use.sr_id
                    return redirect('/faculty_home/')
                elif data.user_type == 'Student':
                    use = Student_register.objects.get(login_id=data.login_id)
                    request.session['student'] = use.sr_id
                    return redirect('/student_home/')
            else:
                messages.error(request, 'Your account is inactive. Please contact administrator.')
                return redirect('/login/')
        except Login.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('/login/')
        except Exception as e:
            messages.error(request, f'Login error: {str(e)}')
            return redirect('/login/')
    return render(request, 'login.html')
    
def master_home(request):
    print("DEBUG: Accessing master_home")
    print("DEBUG: Session data:", dict(request.session))
    
    if 'master' not in request.session:
        print("DEBUG: No master in session, redirecting to login")
        return redirect('login')
    
    return render(request, 'master/index.html')

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
        # Check and update current academic year
        check_and_update_academic_year()
        
        # Get current date for template
        current_date = timezone.now().date()
        
        # Get all academic years ordered by start year (most recent first)
        data = Academic_year.objects.annotate(
            start_year=Cast(Substr('academic_year', 1, 4), output_field=IntegerField())
        ).order_by('-start_year')
        
        return render(request, 'master/academic_year.html', {
            'data': data,
            'current_date': current_date
        })
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
        try:
            # Get the new academic year
            new_ay = Academic_year.objects.get(ay_id=request.GET['ay_id'])
            
            # Get the current academic year
            current_ay = Academic_year.objects.filter(current_ay=True).first()
            
            if current_ay and current_ay != new_ay:
                # Get all students
                students = Student_register.objects.select_related('standard', 'standard__educational_level').all()
                
                # Process each student for promotion
                for student in students:
                    if student.standard:
                        # Get the next standard in the same educational level
                        try:
                            next_standard = Standard.objects.get(
                                educational_level=student.standard.educational_level,
                                standard=student.standard.standard + 1
                            )
                            
                            # Create promotion record
                            StudentPromotion.objects.create(
                                student=student,
                                from_standard=student.standard,
                                to_standard=next_standard,
                                academic_year=new_ay
                            )
                            
                            # Update student's standard
                            student.standard = next_standard
                            student.save()
                            
                        except Standard.DoesNotExist:
                            # Check if there's a next educational level
                            current_el_id = student.standard.educational_level.el_id
                            next_el = Educational_level.objects.filter(
                                el_id__gt=current_el_id
                            ).order_by('el_id').first()  # Get the next level by ID
                            
                            if next_el:
                                # Get the first standard of next educational level
                                next_standard = Standard.objects.filter(
                                    educational_level=next_el
                                ).order_by('standard').first()
                                
                                if next_standard:
                                    # Create promotion record
                                    StudentPromotion.objects.create(
                                        student=student,
                                        from_standard=student.standard,
                                        to_standard=next_standard,
                                        academic_year=new_ay
                                    )
                                    
                                    # Update student's standard
                                    student.standard = next_standard
                                    student.save()
            
            # Update academic year status
            new_ay.current_ay = True
            new_ay.save()
            Academic_year.objects.exclude(ay_id=request.GET['ay_id']).update(current_ay=False)
            
            messages.success(request, 'Academic year updated and students promoted successfully')
            
        except Exception as e:
            messages.error(request, f'Error updating academic year: {str(e)}')
            
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
    if 'master' not in request.session:
        return redirect('/home/')
        
    try:
        if request.method == 'POST':
            email = request.POST['email']
            name = request.POST['name']
            user_type = request.POST['user_type']
            designation_id = request.POST['designation_id']
            
            # Generate random password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Create login
            login = Login.objects.create(
                username=email,
                password=password,
                user_type=user_type,
                status=True
            )
            
            # Create staff record
            Staff_register.objects.create(
                login=login,
                designation_id=designation_id,
                name=name,
                contact_number=None,
                address=None,
                image=None
            )
            
            # Send email with credentials
            try:
                email_sender =  settings.EMAIL
                email_password = settings.MAIL_PASSWORD
                
                body = f"""Dear {name},
                
Your staff account has been created with the following credentials:
Username: {email}
Password: {password}

Please login and change your password.
"""
                
                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email
                em['Subject'] = "Staff Account Credentials"
                em.set_content(body)
                
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email, em.as_string())
                    
                messages.success(request, 'Staff registered successfully. Credentials sent to email.')
            except Exception as e:
                messages.warning(request, f'Staff registered but failed to send email: {str(e)}')
            
            return redirect('staff_register')
            
        designations = Designation.objects.filter(status=True)
        return render(request, 'master/staff_register.html', {'designation': designations})
        
    except Exception as e:
        messages.error(request, f'Error registering staff: {str(e)}')
        return redirect('staff_register')

def staff_status(request):
    if 'master' in request.session:
        data = Login.objects.get(login_id=request.GET['login_id'])
        data.status = request.GET['status']
        data.save()
        messages.success(request, 'Status updated successfully')
        return redirect('/staff_list/')
    else:
        return redirect('/home/')

def get_blockchain():
    return Blockchain()  # No need for cache anymore since we're using database

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
                im = request.FILES['image']
                ob = FileSystemStorage()
                fl = ob.save(im.name, im)
                obj.image = ob.url(fl)
            obj.save()

            # Get standard details
            standard = Standard.objects.get(s_id=request.POST['standard_id'])

            # Add student data to blockchain
            blockchain = get_blockchain()
            current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            student_data = {
                "student_id": obj.sr_id,
                "name": obj.name,
                "email": obj.email,
                "contact": obj.contact_number,
                "address": obj.address,
                "standard": standard.standard,
                "educational_level": standard.educational_level.level,
                "gender": obj.gender,
                "username": obj.login.username,
                "registration_time": current_time
            }
            blockchain.add_block(student_data)

            messages.success(request, 'Registered successfully.')
            return redirect('/student_register/')
    else:
        dt = Standard.objects.select_related('educational_level')
        return render(request,'office_staff/student_register.html',{'standard':dt})


def student_list(request):
    data = Student_register.objects.select_related('login','standard').order_by('-sr_id')
    std = Standard.objects.select_related('educational_level')
    if 'office_staff' in request.session:
        return render(request,'office_staff/student_list.html',{'data':data,'std':std})
    elif 'master' in request.session:
        return render(request,'master/student_list.html',{'data':data,'std':std})
    else:
        return redirect('/home/')
    
def search_student(request):
    str1 = ''
    data = Student_register.objects.filter(standard_id=request.GET.get('id')).select_related('login','standard').order_by('-sr_id')
    if data:
        c = 0
        for i in data:
            c=c+1
            str1 +=f'''<tr>
                        <td>{c}</td>
                        <td><img src="{i.image}" class="rounded" style="height: 60px; width:60px;" alt=""></td>
                        <td>{i.name}</td>
                        <td>
                            Email : {i.login.username} <br>
                            Contact number : {i.contact_number} <br>
                            Address : {i.address}
                        </td>
                        <td>
                            EL - { i.standard.educational_level.level } <br>
                            STD - { i.standard.standard }
                        </td>
                        <td>'''
                            
            if i.login.status == True:
                str1 += f'<a href="/student_status?login_id={i.login_id}&status=0" class="btn btn-danger btn-xs">Dinial Access</a>'
            else:
                str1 += f'<a href="/student_status?login_id={i.login_id}&status=1" class="btn btn-success btn-xs">Allow Access</a>'
            
                                
            str1+=f'''</td>
            </tr>'''
    else:
        str1+= '<tr><td colspan="6"><b class="font-monospace text-danger">Not found any student</b></td></tr>'
    return HttpResponse(str1)








def student_status(request):
    if not 'master' in request.session:
        return redirect('/home/')
    
    try:
        if 'login_id' in request.GET and 'status' in request.GET:
            login = Login.objects.get(login_id=request.GET['login_id'])
            login.status = bool(int(request.GET['status']))  # Convert string to boolean
            login.save()
            
            status_text = "allowed" if login.status else "denied"
            messages.success(request, f'Access has been {status_text} successfully')
        else:
            messages.error(request, 'Invalid request parameters')
            
        return redirect('/student_list/')
    except Login.DoesNotExist:
        messages.error(request, 'Student login not found')
        return redirect('/student_list/')
    except Exception as e:
        messages.error(request, f'Error updating status: {str(e)}')
        return redirect('/student_list/')

def leave_apply(request):
    if 'login_id' not in request.session:
        return redirect('/home/')
        
    try:
        # Get current academic year
        current_ay = Academic_year.objects.get(current_ay=True)
        staff_id = request.session.get('staff_id')
        
        if not staff_id:
            messages.error(request, "Invalid staff member")
            return redirect('/home/')

        if request.method == 'POST':
            try:
                # Get leave details
                leave_type = Leave_type.objects.get(lt_id=request.POST['leave_type_id'])
                start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
                
                # Validate dates
                if start_date > end_date:
                    messages.error(request, 'End date cannot be before start date')
                    return redirect('/leave_apply/')
                
                # Calculate working days
                no_of_days = 0
                current_date = start_date
                while current_date <= end_date:
                    if current_date.weekday() < 5:  # Skip weekends
                        no_of_days += 1
                    current_date += timedelta(days=1)

                if no_of_days == 0:
                    messages.error(request, 'Selected dates only include weekends')
                    return redirect('/leave_apply/')

                # Check for overlapping leaves
                if Staff_leave.objects.filter(
                    staff_id=staff_id,
                    start_date__lte=end_date,
                    end_date__gte=start_date
                ).exists():
                    messages.error(request, 'You already have leave scheduled for these dates')
                    return redirect('/leave_apply/')

                # Create leave request
                Staff_leave.objects.create(
                    staff_id=staff_id,
                    leave_type=leave_type,
                    reason=request.POST['reason'],
                    start_date=start_date,
                    end_date=end_date,
                    no_of_days=no_of_days,
                    academic_year=current_ay
                )
                
                messages.success(request, 'Leave request submitted successfully')
                return redirect('/leave_apply/')
                
            except Leave_type.DoesNotExist:
                messages.error(request, 'Invalid leave type selected')
                return redirect('/leave_apply/')
            except Exception as e:
                messages.error(request, f'Error submitting leave request: {str(e)}')
                return redirect('/leave_apply/')

        # For GET request, prepare leave types with their balances
        leave_types = Leave_type.objects.filter(status=True)
        
        # Calculate remaining leaves for each type
        for leave_type in leave_types:
            taken_leaves = Staff_leave.objects.filter(
                staff_id=staff_id,
                leave_type=leave_type,
                academic_year=current_ay,
                status='Approved'
            ).aggregate(
                total_days=models.Sum('no_of_days')
            )['total_days'] or 0
            
            leave_type.remaining_days = leave_type.days - taken_leaves

        template = None
        if 'accountant' in request.session:
            template = 'accountant/leave_apply.html'
        elif 'office_staff' in request.session:
            template = 'office_staff/leave_apply.html'
        elif 'faculty' in request.session: 
            template = 'faculty/leave_apply.html'
            
        if template:
            return render(request, template, {
                'data': leave_types,
                'current_ay': current_ay
            })
            
        return redirect('/home/')
        
    except Academic_year.DoesNotExist:
        messages.error(request, 'No active academic year found')
        return redirect('/home/')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('/home/')

def new_leave_request(request):
    if not 'master' in request.session:
        return redirect('/home/')
    
    try:
        # Get pending leave requests
        data = Staff_leave.objects.select_related(
            'staff',
            'leave_type'
        ).filter(
            status=None
        ).order_by('-created_at')
        
        context = {
            'data': data,
            'title': 'New Leave Requests'
        }
        return render(request, 'master/new_leave_request.html', context)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
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
    if not 'login_id' in request.session:
        return redirect('/home/')
    
    try:
        if 'master' in request.session:
            # For admin, show all processed leave requests
            data = Staff_leave.objects.select_related(
                'staff', 
                'leave_type'
            ).filter(
                ~Q(status=None)  # Show all requests except pending ones
            ).order_by('-created_at')
            template = 'master/leave_list.html'
        elif 'accountant' in request.session:
            data = Staff_leave.objects.select_related(
                'leave_type'
            ).filter(
                staff_id=request.session['accountant']
            ).order_by('-created_at')
            template = 'accountant/leave_list.html'
        elif 'office_staff' in request.session:
            data = Staff_leave.objects.select_related(
                'leave_type'
            ).filter(
                staff_id=request.session['office_staff']
            ).order_by('-created_at')
            template = 'office_staff/leave_list.html'
        elif 'faculty' in request.session:
            data = Staff_leave.objects.select_related(
                'leave_type'
            ).filter(
                staff_id=request.session['faculty']
            ).order_by('-created_at')
            template = 'faculty/leave_list.html'
        else:
            messages.error(request, 'Invalid user type')
            return redirect('/home/')

        context = {
            'data': data,
            'title': 'Leave History'
        }
        return render(request, template, context)
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
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
        data = School_finance.objects.all().order_by('account_category')
        return render(request, 'master/school_finance.html', {'data': data})
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
            return render(request, 'accountant/salary_table.html', {
                'data': data,
                'des': des
            })
    elif 'master' in request.session:
        data = Salary_table.objects.select_related('designation')
        return render(request, 'master/salary_table.html', {'data': data})
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
    if not ('master' in request.session or 'accountant' in request.session):
        print("DEBUG: User not logged in as master or accountant")
        return redirect('login')
    
    if request.method == 'POST':
        try:
            print("DEBUG: Processing POST request")
            educational_level_id = request.POST['educational_level_id']
            fee_type = request.POST['fee_type']
            amount = float(request.POST['amount'])
            term = request.POST['term']

            # Check if fee already exists
            exists = Student_fee.objects.filter(
                educational_level_id=educational_level_id,
                fee_type=fee_type,
                term=term,
                status=True
            ).exists()
            
            if exists:
                messages.error(request, f"'{fee_type}' already exists for this educational level and term!")
                return redirect('student_fee')

            # Validate fee limits
            try:
                fee_limit = FeeLimit.objects.get(
                    educational_level_id=educational_level_id,
                    fee_type=fee_type,
                    status=True
                )
                
                if amount < fee_limit.lower_limit:
                    messages.error(request, f"Amount cannot be below ₹{fee_limit.lower_limit}")
                    return redirect('student_fee')
                
                if amount > fee_limit.upper_limit:
                    messages.error(request, f"Amount cannot exceed ₹{fee_limit.upper_limit}")
                    return redirect('student_fee')
                
            except FeeLimit.DoesNotExist:
                messages.error(request, "No fee limits found for this combination")
                return redirect('student_fee')
            
            # Create new fee if validation passes
            Student_fee.objects.create(
                account_category=request.POST.get('account_category', 'Income'),
                educational_level_id=educational_level_id,
                fee_type=fee_type,
                term=term,
                amount=amount,
                status=True
            )
            
            messages.success(request, 'Fee structure added successfully!')
            return redirect('student_fee')
            
        except Exception as e:
            print("DEBUG: Error in POST:", str(e))
            messages.error(request, f'Error adding fee structure: {str(e)}')
            return redirect('student_fee')
    
    try:
        print("DEBUG: Processing GET request")
        # Get all educational levels without status filter
        edl = Educational_level.objects.all().order_by('level')
        
        # Get all fees with related educational level data
        data = Student_fee.objects.select_related('educational_level').all().order_by(
            'educational_level__level', 'term', 'fee_type'
        )
        
        # Calculate totals for each educational level
        level_totals = {}
        for fee in data:
            if fee.status:  # Only include active fees
                level_id = fee.educational_level.el_id
                level_totals[level_id] = level_totals.get(level_id, 0) + fee.amount
        
        context = {
            'edl': edl,
            'data': data,
            'level_totals': level_totals,
            'last_added_level': request.GET.get('last_level')
        }
        
        template = 'master/student_fee.html' if 'master' in request.session else 'accountant/student_fee.html'
        return render(request, template, context)
        
    except Exception as e:
        print("DEBUG: Error in GET:", str(e))
        messages.error(request, f'Error loading fee structures: {str(e)}')
        return redirect('home')

def edit_student_fee(request):
    if not ('master' in request.session or 'accountant' in request.session):
        return redirect('login')
    
    try:
        if request.method == 'POST':
            fee = Student_fee.objects.get(sf_id=request.POST['sf_id'])
            
            # Check for duplicates
            exists = Student_fee.objects.filter(
                educational_level_id=request.POST['educational_level_id'],
                fee_type=request.POST['fee_type'],
                term=request.POST['term'],
                status=True
            ).exclude(sf_id=fee.sf_id).exists()
            
            if exists:
                messages.error(request, f"'{request.POST['fee_type']}' already exists for this educational level and term!")
                return redirect('student_fee')
            
            # Update fee
            fee.educational_level_id = request.POST['educational_level_id']
            fee.fee_type = request.POST['fee_type']
            fee.term = request.POST['term']
            fee.amount = request.POST['amount']
            fee.save()
            
            messages.success(request, 'Fee structure updated successfully!')
            return redirect('student_fee')
        
        # Get fee data for edit form
        fee = Student_fee.objects.get(sf_id=request.GET['id'])
        edl = Educational_level.objects.all().order_by('level')  # Removed status filter
        
        context = {
            'fee': fee,
            'edl': edl
        }
        
        # Use appropriate template based on user role
        template = 'master/edit_student_fee.html' if 'master' in request.session else 'accountant/edit_student_fee.html'
        return render(request, template, context)
        
    except Student_fee.DoesNotExist:
        messages.error(request, 'Fee structure not found!')
        return redirect('student_fee')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('student_fee')

def status_student_fee(request):
    if not ('master' in request.session or 'accountant' in request.session):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
    
    try:
        fee = Student_fee.objects.get(sf_id=request.GET['sf_id'])
        fee.status = request.GET['status'] == '1'
        fee.save()
        messages.success(request, 'Status updated successfully')
        return redirect('student_fee')
    except Student_fee.DoesNotExist:
        messages.error(request, 'Fee not found')
        return redirect('student_fee')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('student_fee')

def check_student_fee_exist(request):
    if not ('master' in request.session or 'accountant' in request.session):
        return JsonResponse({'exists': True})
    
    try:
        exists = Student_fee.objects.filter(
            educational_level_id=request.GET['educational_level_id'],
            fee_type=request.GET['fee_type'],
            term=request.GET['term'],
            status=True
        ).exists()
        return JsonResponse({'exists': exists})
    except Exception:
        return JsonResponse({'exists': True})

def student_fee_transactions(request):
    if 'accountant' in request.session or 'master' in request.session:
        try:
            # Get all transactions without payment_status filter
            data = Student_fee_transaction.objects.select_related(
                'student',
                'student__standard',
                'student__login',
                'academic_year',
                'student_fee'
            ).order_by('-payment_date')

            # Get active academic years
            ay = Academic_year.objects.filter(status=True)

            # Get all standards
            std = Standard.objects.select_related('educational_level').all()

            context = {
                'data': data,
                'ay': ay,
                'std': std,
                'title': 'Student Fee Transactions'
            }

            template = 'master/student_fee_transactions.html' if 'master' in request.session else 'accountant/student_fee_transactions.html'
            return render(request, template, context)

        except Exception as e:
            import traceback
            print("Error in student_fee_transactions:", str(e))
            print(traceback.format_exc())
            messages.error(request, f'Error loading transactions: {str(e)}')
            return redirect('home')
    else:
        messages.error(request, 'Access denied')
        return redirect('home')

def staff_salary(request):
    if 'accountant' not in request.session:
        return redirect('/home/')
    
    try:
        current_ay = Academic_year.objects.get(current_ay=True)
        context = {
            'title': 'Staff Salary',
            'ay': current_ay,
            'json_data': f"{current_ay.start_date.year}-{current_ay.end_date.year}"
        }
        return render(request, 'accountant/staff_salary.html', context)
    except Academic_year.DoesNotExist:
        messages.error(request, 'Please set up current academic year first')
        return render(request, 'accountant/staff_salary.html', {'title': 'Staff Salary'})

def search_staff_salary(request):
    if 'accountant' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        month_year = request.GET.get('chdate')
        if not month_year:
            return HttpResponse('Please select a month')
            
        year, month = map(int, month_year.split('-'))
        first_day = datetime(year, month, 1).date()
        if month == 12:
            last_day = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1).date() - timedelta(days=1)
            
        # Get all staff members
        staff_list = Staff_register.objects.select_related('designation').filter(
            login__status=True
        )
        
        salary_data = []
        # Calculate total working days (excluding weekends)
        total_days = 0
        current = first_day
        while current <= last_day:
            if current.weekday() < 5:  # Monday = 0, Sunday = 6
                total_days += 1
            current += timedelta(days=1)
        
        for staff in staff_list:
            try:
                # Get salary components
                salary_info = Salary_table.objects.get(designation=staff.designation)
                basic_pay = salary_info.basic_pay
                da_amount = (basic_pay * salary_info.da) / 100
                hra_amount = (basic_pay * salary_info.hra) / 100
                ta_amount = (basic_pay * salary_info.ta) / 100
                agp_amount = (basic_pay * salary_info.agp) / 100
                
                # Calculate total monthly salary
                total_monthly_salary = basic_pay + da_amount + hra_amount + ta_amount + agp_amount
                
                # Calculate per day salary based on working days
                per_day_salary = total_monthly_salary / total_days
                
                # Get total absences
                absences = StaffAttendance.objects.filter(
                    staff=staff,
                    attendance_date__range=[first_day, last_day],
                    attendance_status__status_name='Absent'
                ).count()
                
                # Get approved leaves
                approved_leaves = Staff_leave.objects.filter(
                    staff=staff,
                    start_date__lte=last_day,
                    end_date__gte=first_day,
                    status='Approved'
                ).select_related('leave_type')
                
                # Calculate leave days that overlap with this month
                approved_leave_days = 0
                for leave in approved_leaves:
                    leave_start = max(leave.start_date, first_day)
                    leave_end = min(leave.end_date, last_day)
                    days = (leave_end - leave_start).days + 1
                    
                    # Count only working days
                    for i in range(days):
                        current_date = leave_start + timedelta(days=i)
                        if current_date.weekday() < 5:  # Skip weekends
                            approved_leave_days += 1
                
                # Calculate actual absences (excluding approved leaves)
                actual_absences = max(0, absences - approved_leave_days)
                
                # Calculate deductions
                absence_deduction = actual_absences * per_day_salary
                
                # Calculate final salary
                final_salary = total_monthly_salary - absence_deduction
                
                salary_data.append({
                    'staff': staff,
                    'salary_components': {
                        'basic_pay': basic_pay,
                        'da': salary_info.da,
                        'da_amount': da_amount,
                        'hra': salary_info.hra,
                        'hra_amount': hra_amount,
                        'ta': salary_info.ta,
                        'ta_amount': ta_amount,
                        'agp': salary_info.agp,
                        'agp_amount': agp_amount
                    },
                    'monthly_salary': total_monthly_salary,
                    'working_days': total_days,
                    'total_absences': absences,
                    'approved_leaves': approved_leave_days,
                    'actual_absences': actual_absences,
                    'per_day_salary': per_day_salary,
                    'absence_deduction': absence_deduction,
                    'final_salary': final_salary
                })
                
            except Salary_table.DoesNotExist:
                continue
                
        context = {
            'salary_data': salary_data,
            'month_year': datetime(year, month, 1).strftime('%B %Y')
        }
        return render(request, 'accountant/staff_salary_table.html', context)
        
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')

def salary_transaction(request):
    if 'accountant' not in request.session:
        return JsonResponse({
            'status': 'error',
            'message': 'Unauthorized access'
        }, status=403)
        
    if request.method == 'POST':
        try:
            print("Received data:", request.POST)  # Debug print
            
            # Validate required fields
            if not request.POST.get('staff_id') or not request.POST.get('salary_date'):
                raise ValueError("Staff ID and salary date are required")
            
            # Get current academic year
            academic_year = Academic_year.objects.get(current_ay=True)
            
            # Get staff and salary table
            staff = Staff_register.objects.get(sr_id=request.POST['staff_id'])
            salary_table = Salary_table.objects.get(
                designation=staff.designation,
                status=True
            )
            
            # Parse salary date
            try:
                date_str = request.POST.get('salary_date', '').strip()
                print(f"Processing date string: {date_str}")  # Debug print
                
                # Split the date string into month and year
                month_name, year = date_str.split()
                month_num = datetime.strptime(month_name, '%B').month
                
                # Create date as YYYY-MM-01
                salary_date = datetime(int(year), month_num, 1).date()
                print(f"Parsed date: {salary_date}")  # Debug print
                
            except Exception as e:
                print(f"Date parsing error: {str(e)}")
                raise ValueError(f"Invalid date format. Expected format: 'Month Year'")
            
            # Check if salary already processed
            if Salary_transaction.objects.filter(
                staff_id=staff.sr_id,
                salary_date__year=salary_date.year,
                salary_date__month=salary_date.month
            ).exists():
                raise ValueError(f"Salary already processed for {month_name} {year}")

            # Calculate salary components
            basic_pay = salary_table.basic_pay
            da_amount = (basic_pay * salary_table.da) / 100
            hra_amount = (basic_pay * salary_table.hra) / 100
            ta_amount = (basic_pay * salary_table.ta) / 100
            agp_amount = (basic_pay * salary_table.agp) / 100
            deductions = float(request.POST.get('deductions', 0))
            
            # Create transaction
            transaction = Salary_transaction(
                staff=staff,
                academic_year=academic_year,
                salary_table=salary_table,
                basic_pay=basic_pay,
                da_amount=da_amount,
                hra_amount=hra_amount,
                ta_amount=ta_amount,
                agp_amount=agp_amount,
                bonus=0,
                deductions=deductions,
                salary_date=salary_date,
                approval_status='Pending'
            )
            
            # Save transaction
            transaction.save()
            print(f"Created salary transaction: {transaction.st_id}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Salary transaction created successfully',
                'transaction_id': transaction.st_id
            })
            
        except ValueError as e:
            print(f"Validation error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        except Exception as e:
            print(f"Error in salary_transaction: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing salary: {str(e)}'
            }, status=500)
    else:
        if 'staff_id' in request.GET and 'dt' in request.GET:
            try:
                # Get staff details
                staff = Staff_register.objects.select_related(
                    'designation',
                    'login'
                ).get(sr_id=request.GET['staff_id'])
                
                # Get salary table
                salary_table = Salary_table.objects.get(
                    designation=staff.designation,
                    status=True
                )
                
                # Get current academic year
                ay = Academic_year.objects.get(current_ay=True)
                
                # Calculate salary components
                basic_pay = salary_table.basic_pay
                da_amount = (basic_pay * salary_table.da) / 100
                hra_amount = (basic_pay * salary_table.hra) / 100
                ta_amount = (basic_pay * salary_table.ta) / 100
                agp_amount = (basic_pay * salary_table.agp) / 100
                
                # Format date
                date_str = request.GET['dt']
                year, month = date_str.split('-')
                formatted_date = f"{year}-{month}-01"
                
                context = {
                    'staff': staff,
                    'ay': ay,
                    'salary_table': salary_table,
                    'dt': formatted_date,
                    'da_amount': da_amount,
                    'hra_amount': hra_amount,
                    'ta_amount': ta_amount,
                    'agp_amount': agp_amount
                }
                return render(request, 'accountant/salary_transaction.html', context)
            except Exception as e:
                messages.error(request, f'Error loading salary form: {str(e)}')
                print(f"Error loading salary form: {str(e)}")
                return redirect('/staff_salary/')
        else:
            return redirect('/staff_salary/')

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
    if 'accountant' in request.session or 'master' in request.session:
        # Get pending and denied salary transactions with all related data
        data = Salary_transaction.objects.filter(
            Q(approval_status='Pending') | Q(approval_status='Denied')
        ).select_related(
            'staff',
            'staff__designation',
            'academic_year',
            'salary_table'
        ).annotate(
            total_salary=F('basic_pay') + F('bonus') + F('da_amount') + 
                        F('hra_amount') + F('ta_amount') + F('agp_amount'),
            payable=F('total_salary') - F('deductions')
        ).order_by('-salary_date')

        template = 'master/salary_transactions_list.html' if 'master' in request.session else 'accountant/salary_transactions_list.html'
        
        context = {
            'data': data,
            'title': 'New Salary Transactions',
            'approval_pending': True
        }
        
        return render(request, template, context)
    else:
        return redirect('/home/')

def salary_transactions_history(request):
    if 'accountant' in request.session or 'master' in request.session:
        # Get approved salary transactions with calculated totals
        data = Salary_transaction.objects.filter(
            approval_status='Approved'
        ).select_related(
            'staff',
            'staff__designation',
            'staff__login',
            'academic_year',
            'salary_table'
        ).annotate(
            total_salary=F('basic_pay') + F('da_amount') + 
                        F('hra_amount') + F('ta_amount') + 
                        F('agp_amount') + F('bonus') - F('deductions')
        ).order_by('-salary_date')

        # Get staff list for filter
        staff = Staff_register.objects.select_related('designation').all()
        
        # Get academic years for filter
        academic_years = Academic_year.objects.filter(status=True)

        template = 'master/salary_transactions_history.html' if 'master' in request.session else 'accountant/salary_transactions_history.html'
        
        context = {
            'data': data,
            'staff': staff,
            'ay': academic_years,
            'title': 'Salary Transaction History'
        }
        
        return render(request, template, context)
    else:
        return redirect('/home/')

def salary_transactions_status(request):
    if 'master' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)
    
    try:
        transaction_id = request.GET.get('sft_id')
        status = request.GET.get('status')
        
        if not transaction_id or status is None:
            raise ValueError("Missing required parameters")
            
        transaction = Salary_transaction.objects.get(st_id=transaction_id)
        
        # Get or create School_finance record for staff salary
        school_finance, created = School_finance.objects.get_or_create(
            account_category='Expense',
            finance_type='Staff Salary',
            defaults={
                'status': True
            }
        )
        
        if status == '1':
            # Calculate total salary and payable amount
            total_salary = (
                transaction.basic_pay +
                transaction.da_amount +
                transaction.hra_amount +
                transaction.ta_amount +
                transaction.agp_amount +
                transaction.bonus
            )
            payable = total_salary - transaction.deductions
            
            transaction.approval_status = 'Approved'
            transaction.payable = payable  # Store the calculated payable amount
            
            # Create finance transaction record
            School_finance_transaction.objects.create(
                academic_year=transaction.academic_year,
                school_finance=school_finance,
                description=f'Salary for {transaction.staff.name} - {transaction.salary_date.strftime("%B %Y")}',
                total_amount=payable,
                entry_date=timezone.now(),
                approval_status='Approved'
            )
            messages.success(request, 'Salary transaction approved successfully')
        else:
            transaction.approval_status = 'Denied'
            messages.success(request, 'Salary transaction denied')
            
        transaction.save()
        
        return redirect('salary_transaction_details', transaction_id=transaction.st_id)
        
    except Salary_transaction.DoesNotExist:
        messages.error(request, 'Salary transaction not found')
        return redirect('new_salary_transactions')
    except School_finance.DoesNotExist:
        messages.error(request, 'School finance configuration not found')
        return redirect('salary_transaction_details', transaction_id=transaction_id)
    except Exception as e:
        messages.error(request, f'Error updating status: {str(e)}')
        return redirect('salary_transaction_details', transaction_id=transaction_id)

def salary_details(request):
    if 'accountant' in request.session or 'master' in request.session:
        try:
            # Check if st_id is in the request parameters
            st_id = request.GET.get('st_id')
            if not st_id:
                messages.error(request, 'No salary transaction ID provided')
                return redirect('/new_salary_transactions/')
            
            # Calculate total salary and payable amount using annotate
            transaction = Salary_transaction.objects.select_related(
                'staff',
                'staff__designation',
                'staff__login',
                'academic_year',
                'salary_table'
            ).annotate(
                total_salary=F('basic_pay') + F('bonus') + F('da_amount') + 
                            F('hra_amount') + F('ta_amount') + F('agp_amount'),
                payable=F('total_salary') - F('deductions')
            ).get(st_id=st_id)
            
            # Calculate total salary for context
            total = (
                transaction.basic_pay +
                transaction.bonus +
                transaction.da_amount +
                transaction.hra_amount +
                transaction.ta_amount +
                transaction.agp_amount
            )
            
            # Set total_salary and payable explicitly
            transaction.total_salary = total
            transaction.payable = total - transaction.deductions
            
            context = {
                'data': transaction,
                'title': 'Salary Transaction Details'
            }
            
            template = 'master/salary_details.html' if 'master' in request.session else 'accountant/salary_details.html'
            return render(request, template, context)
            
        except Salary_transaction.DoesNotExist:
            messages.error(request, 'Salary transaction not found')
            return redirect('/new_salary_transactions/')
        except Exception as e:
            messages.error(request, f'Error loading salary details: {str(e)}')
            return redirect('/new_salary_transactions/')
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
    try:
        str1 = ''
        
        # Build query conditions
        ay_query = Q(academic_year_id=request.GET['ay_id']) if request.GET.get('ay_id') else Q()
        std_query = Q(student__standard_id=request.GET['s_id']) if request.GET.get('s_id') else Q()
        month_query = Q(payment_date__month=request.GET['my']) if request.GET.get('my') else Q()

        data = Student_fee_transaction.objects.filter(
            ay_query, 
            std_query,
            month_query
        ).select_related(
            'student',
            'student__standard',
            'student__login',
            'academic_year',
            'student_fee'
        ).order_by('-payment_date')

        if data:
            for index, transaction in enumerate(data, 1):
                str1 += f'''
                <tr>
                    <td>{index}</td>
                    <td>
                        <img src="{transaction.student.image}" class="rounded" style="height: 60px; width:60px;" alt=""><br>
                        <strong>{transaction.student.name}</strong><br>
                        Class: {transaction.student.standard.standard}<br>
                        Contact: {transaction.student.contact_number}
                    </td>
                    <td>
                        Type: {transaction.student_fee.fee_type}<br>
                        Amount: ₹{transaction.total_amount}<br>
                        Academic Year: {transaction.academic_year.academic_year}
                    </td>
                    <td>
                        Date: {transaction.payment_date.strftime("%d %b %Y")}<br>
                        Time: {transaction.created_at.strftime("%I:%M %p")}<br>
                        {f"Payment ID: {transaction.razorpay_payment_id}" if transaction.razorpay_payment_id else ""}
                    </td>
                    <td>
                        <a href="/fee_pdf?sft_id={transaction.sft_id}" 
                           class="btn btn-info btn-sm">
                            <i class="fas fa-file-pdf"></i> Download Receipt
                        </a>
                    </td>
                </tr>'''
        else:
            str1 = '<tr><td colspan="5" class="text-center">No fee transactions found</td></tr>'

        return HttpResponse(str1)
        
    except Exception as e:
        return HttpResponse(f'<tr><td colspan="5" class="text-center text-danger">Error: {str(e)}</td></tr>')


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
        try:
            # Parse date from request
            chdate = request.GET['dt']
            year, month = map(int, chdate.split('-'))
            selected_date = date(year, month, calendar.monthrange(year, month)[1])  # Last day of selected month
        
            # Get standard and its educational level
            standard_id = request.GET.get('s_id')
            standard = Standard.objects.select_related('educational_level').get(pk=standard_id)
            
            # Get current academic year
            current_ay = Academic_year.objects.get(current_ay=True)
            
            # Get all students in the standard
            students = Student_register.objects.filter(standard=standard).select_related(
                'standard', 
                'standard__educational_level'
            )

            # Get all fees for the educational level
            fees = Student_fee.objects.filter(
                educational_level=standard.educational_level,
                status=True
            )

            # Calculate term based on month
            if 6 <= month <= 8:
                current_term = '1'  # First term
            elif 9 <= month <= 11:
                current_term = '2'  # Second term
            else:
                current_term = '3'  # Third term

            # Parse academic year
            start_year = int(current_ay.academic_year.split('-')[0])
            end_year = start_year + 1

            student_data = []  

            for student in students:
                # Get all fees paid by this student before or in the selected month
                paid_fees = Student_fee_transaction.objects.filter(
                    student=student,
                    academic_year=current_ay,
                    payment_date__lte=selected_date
                ).values_list('student_fee_id', flat=True)

                # Get unpaid fees
                unpaid_fees = []
                total_dues = 0
                
                for fee in fees:
                    # Skip if fee is already paid
                    if fee.sf_id in paid_fees:
                        continue
                        
                    # Skip if fee is for a future term based on selected month
                    if (current_term == '1' and fee.term in ['2', '3']) or \
                       (current_term == '2' and fee.term == '3'):
                        continue

                    # Calculate due date based on term
                    if fee.term == '1':
                        due_date = date(start_year, 8, 31)  # August 31st
                    elif fee.term == '2':
                        due_date = date(start_year, 11, 30)  # November 30th
                    else:
                        due_date = date(end_year, 3, 31)  # March 31st

                    # Calculate late fee if applicable
                    is_overdue = selected_date > due_date
                    late_fee = 0
                    if is_overdue:
                        days_late = (selected_date - due_date).days
                        late_fee = days_late * 10  # ₹10 per day

                    total_amount = fee.amount + late_fee
                    total_dues += total_amount

                    unpaid_fees.append({
                        'fee_type': fee.fee_type,
                        'base_amount': fee.amount,
                        'late_fee': late_fee,
                        'total_amount': total_amount,
                        'due_date': due_date,
                        'days_overdue': (selected_date - due_date).days if is_overdue else 0,
                        'is_overdue': is_overdue,
                        'term': fee.term
                    })

                if unpaid_fees:  # Only add students with unpaid fees
                    student_data.append({
                        'student': student,
                        'unpaid_fees': unpaid_fees,
                        'total_dues': total_dues
                    })
        
            str1 = ''
            if student_data:
                str1 += '''
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Student Details</th>
                                    <th>Unpaid Fees</th>
                                    <th>Total Due Amount</th>
                                </tr>
                            </thead>
                            <tbody>
                '''
                for index, data in enumerate(student_data, 1):
                    student = data['student']
                    str1 += f'''
                        <tr>
                            <td>{index}</td>
                            <td>
                                <img src="{student.image}" class="rounded" style="height: 60px; width:60px;" alt=""><br>
                                <strong>{student.name}</strong><br>
                                Class: {student.standard.standard}<br>
                                Contact: {student.contact_number}
                            </td>
                            <td>
                                <table class="table table-sm mb-0">
                                    <thead>
                                        <tr>
                                            <th>Fee Type</th>
                                            <th>Term</th>
                                            <th>Base Amount</th>
                                            <th>Late Fee</th>
                                            <th>Total</th>
                                            <th>Due Date</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                    '''
                    
                    for fee in data['unpaid_fees']:
                        term_names = {
                            '1': 'First Term',
                            '2': 'Second Term',
                            '3': 'Third Term'
                        }
                        
                        # Format the late fee display
                        late_fee_display = f"₹{fee['late_fee']}" if fee['late_fee'] > 0 else "-"
                        status_display = "Overdue" if fee['is_overdue'] else "Due"
                        status_class = "text-danger" if fee['is_overdue'] else "text-warning"
                        
                        str1 += f'''
                            <tr {' class="table-warning"' if fee['is_overdue'] else ''}>
                                <td>{fee['fee_type']}</td>
                                <td>{term_names[fee['term']]}</td>
                                <td>₹{fee['base_amount']}</td>
                                <td>{late_fee_display}</td>
                                <td>₹{fee['total_amount']}</td>
                                <td>
                                    {fee['due_date'].strftime('%d %b %Y')}
                                    {f"<br><small class='text-danger'>({fee['days_overdue']} days overdue)</small>" if fee['is_overdue'] else ""}
                                </td>
                                <td><span class="{status_class}">{status_display}</span></td>
                            </tr>
                        '''
            
                    str1 += f'''
                                    </tbody>
                                </table>
                            </td>
                            <td class="text-right">
                                <strong>₹{data['total_dues']}</strong>
                            </td>
                        </tr>
                    '''
                
                str1 += '''
                        </tbody>
                    </table>
                    </div>
                '''
            else:
                str1 += '<div class="alert alert-info">No unpaid fees found for this class in the selected month.</div>'

            return HttpResponse(str1)

        except Exception as e:
            return HttpResponse(f'<div class="alert alert-danger">Error: {str(e)}</div>')
    else:
        data = Standard.objects.select_related('educational_level')
        template_name = 'accountant/student_fee_dues.html' if 'accountant' in request.session else 'master/student_fee_dues.html'
        return render(request, template_name, {'std': data})

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
    try:
        # Initialize variables
        student_fee = 0
        staff_salary = 0
        other_income = 0
        other_expense = 0
        pdfurlpath = "/school_transactions_pdf?s="

        # Get academic year filter
        ay_id = request.GET.get('ay_id')
        if ay_id:
            ay_query = Q(academic_year_id=ay_id)
            pdfurlpath += f"&ay_id={ay_id}"
        else:
            ay_query = Q()

        # Get month range filters
        start_month = request.GET.get('sm')
        end_month = request.GET.get('em')

        # Build date queries based on month filters
        if start_month and end_month:
            date_range = Q(
                payment_date__month__range=(start_month, end_month),
                payment_date__year=timezone.now().year
            )
            salary_range = Q(
                salary_date__month__range=(start_month, end_month),
                salary_date__year=timezone.now().year
            )
            entry_range = Q(
                entry_date__month__range=(start_month, end_month),
                entry_date__year=timezone.now().year
            )
            pdfurlpath += f"&sm={start_month}&em={end_month}"
        elif start_month:
            date_range = Q(
                payment_date__month=start_month,
                payment_date__year=timezone.now().year
            )
            salary_range = Q(
                salary_date__month=start_month,
                salary_date__year=timezone.now().year
            )
            entry_range = Q(
                entry_date__month=start_month,
                entry_date__year=timezone.now().year
            )
            pdfurlpath += f"&sm={start_month}"
        else:
            date_range = Q()
            salary_range = Q()
            entry_range = Q()

        # Get student fee income
        if ay_id:
            student_fee = Student_fee_transaction.objects.filter(
                ay_query, date_range
            ).aggregate(
                total=Sum('total_amount')
            )['total'] or 0

        # Get approved staff salary expenses
        if ay_id:
            salary_queryset = Salary_transaction.objects.filter(
                ay_query, 
                salary_range,
                approval_status='Approved'
            )
            if salary_queryset.exists():
                staff_salary = salary_queryset.aggregate(
                    total=Sum(F('basic_pay') + F('da_amount') + F('hra_amount') + 
                            F('ta_amount') + F('agp_amount') + F('bonus') - F('deductions'))
                )['total'] or 0

        # Get other approved transactions
        if ay_id:
            # Income
            other_income = School_finance_transaction.objects.filter(
                ay_query,
                entry_range,
                school_finance__account_category='Income',
                approval_status='Approved'
            ).aggregate(
                total=Sum('total_amount')
            )['total'] or 0

            # Expenses
            other_expense = School_finance_transaction.objects.filter(
                ay_query,
                entry_range,
                school_finance__account_category='Expense',
                approval_status='Approved'
            ).aggregate(
                total=Sum('total_amount')
            )['total'] or 0

        # Calculate totals
        total_income = float(student_fee) + float(other_income)
        total_expense = float(staff_salary) + float(other_expense)
        net_balance = total_income - total_expense

        # Generate response HTML
        response_html = f'''
        <div class="card">
            <h5 class="card-header">Transaction Summary</h5>
            <div class="card-body">
                <div class="mb-2">
                    <a href="{pdfurlpath}" class="btn btn-sm btn-outline-danger float-right">
                        <i class="fas fa-file-pdf"></i> Download PDF
                    </a>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="card border-success">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0">Income</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-sm">
                                    <tr>
                                        <td>Student Fees</td>
                                        <td class="text-right">₹{student_fee:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td>Other Income</td>
                                        <td class="text-right">₹{other_income:,.2f}</td>
                                    </tr>
                                    <tr class="table-success font-weight-bold">
                                        <td>Total Income</td>
                                        <td class="text-right">₹{total_income:,.2f}</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card border-danger">
                            <div class="card-header bg-danger text-white">
                                <h5 class="mb-0">Expenses</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-sm">
                                    <tr>
                                        <td>Staff Salaries</td>
                                        <td class="text-right">₹{staff_salary:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td>Other Expenses</td>
                                        <td class="text-right">₹{other_expense:,.2f}</td>
                                    </tr>
                                    <tr class="table-danger font-weight-bold">
                                        <td>Total Expenses</td>
                                        <td class="text-right">₹{total_expense:,.2f}</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card border-primary">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Net Balance</h5>
                    </div>
                    <div class="card-body">
                        <h3 class="text-center {('text-success' if net_balance >= 0 else 'text-danger')}">
                            ₹{net_balance:,.2f}
                        </h3>
                    </div>
                </div>
            </div>
        </div>
        '''
        
        return HttpResponse(response_html)
        
    except Exception as e:
        print(f"Error in school_transactions_search: {str(e)}")
        return HttpResponse(
            '<div class="alert alert-danger">Error loading transaction data. Please try again.</div>'
        )

def school_transactions_pdf(request):
    try:
        # Initialize variables
        student_fees = 0
        staff_salaries = 0
        other_income = 0
        other_expense = 0

        # Build queries
        ay_query = Q(academic_year_id=request.GET.get('ay_id')) if 'ay_id' in request.GET else Q()
        
        # Build date range queries
        if 'sm' in request.GET and 'em' in request.GET:
            date_range = Q(payment_date__month__range=(request.GET['sm'], request.GET['em']))
            salary_range = Q(salary_date__month__range=(request.GET['sm'], request.GET['em']))
            entry_range = Q(entry_date__month__range=(request.GET['sm'], request.GET['em']))
        elif 'sm' in request.GET:
            date_range = Q(payment_date__month=request.GET['sm'])
            salary_range = Q(salary_date__month=request.GET['sm'])
            entry_range = Q(entry_date__month=request.GET['sm'])
        else:
            date_range = Q()
            salary_range = Q()
            entry_range = Q()

        # Get student fees
        student_fees = Student_fee_transaction.objects.filter(
            ay_query, 
            date_range
        ).aggregate(
            total_amount=Sum('total_amount')
        )['total_amount'] or 0

        # Get approved staff salaries with calculated total
        salary_total = Salary_transaction.objects.filter(
            ay_query,
            salary_range,
            approval_status='Approved'
        ).aggregate(
            total_amount=Sum(
                F('basic_pay') + F('da_amount') + F('hra_amount') + 
                F('ta_amount') + F('agp_amount') + F('bonus') - F('deductions')
            )
        )['total_amount'] or 0

        # Get other income
        other_income = School_finance_transaction.objects.filter(
            ay_query,
            entry_range,
            school_finance__account_category='Income',
            approval_status='Approved'
        ).aggregate(
            total_amount=Sum('total_amount')
        )['total_amount'] or 0

        # Get other expenses
        other_expense = School_finance_transaction.objects.filter(
            ay_query,
            entry_range,
            school_finance__account_category='Expense',
            approval_status='Approved'
        ).aggregate(
            total_amount=Sum('total_amount')
        )['total_amount'] or 0

        # Calculate totals
        total_income = float(student_fees) + float(other_income)
        total_expense = float(salary_total) + float(other_expense)
        net_balance = total_income - total_expense

        # Get academic year info for header
        academic_year = None
        if 'ay_id' in request.GET:
            academic_year = Academic_year.objects.get(ay_id=request.GET['ay_id'])

        # Prepare context for PDF
        context = {
            'academic_year': academic_year,
            'date_range': {
                'start_month': request.GET.get('sm'),
                'end_month': request.GET.get('em')
            },
            'income': {
                'student_fees': student_fees,
                'other_income': other_income,
                'total': total_income
            },
            'expense': {
                'staff_salaries': salary_total,
                'other_expense': other_expense,
                'total': total_expense
            },
            'net_balance': net_balance
        }

        # Generate PDF
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="school_transactions.pdf"'
        
        html = render_to_string('school_transactions_pdf.html', context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF')

        return response

    except Exception as e:
        print(f"Error generating transactions PDF: {str(e)}")
        return HttpResponse('Error generating PDF')

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
    current_sf_id = request.GET.get('current_sf_id')
    query = Student_fee.objects.filter(
        educational_level_id=request.GET.get('educational_level_id'),
        fee_type=request.GET.get('fee_type'),
        term=request.GET.get('term'),
        status=True
    )
    
    # If checking during edit, exclude the current fee being edited
    if current_sf_id:
        query = query.exclude(sf_id=current_sf_id)
    
    exists = query.exists()
    return JsonResponse({'exists': exists})

def get_fee_limits(request):
    """Get fee limits for a specific education level and fee type"""
    try:
        educational_level_id = request.GET.get('educational_level_id')
        fee_type = request.GET.get('fee_type')
        
        fee_limit = FeeLimit.objects.get(
            educational_level_id=educational_level_id,
            fee_type=fee_type,
            status=True
        )
        
        return JsonResponse({
            'success': True,
            'lower_limit': fee_limit.lower_limit,
            'upper_limit': fee_limit.upper_limit
        })
    except FeeLimit.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No fee limits found for this combination'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def sign_out(request):
    try:
        # Clear all session data
        request.session.flush()
        messages.success(request, 'You have been successfully logged out.')
    except Exception as e:
        messages.error(request, f'Logout error: {str(e)}')
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

def blockchain_view(request):
    if 'master' in request.session:
        blockchain = get_blockchain()
        blocks = blockchain.get_all_blocks()
        return render(request, 'master/blockchain_view.html', {
            'blocks': blocks,
            'total_blocks': len(blocks) - 1  # Subtract genesis block
        })
    else:
        return redirect('/home/')

def edit_salary_transaction(request):
    if 'accountant' in request.session:
        if request.method == 'POST':
            try:
                obj = Salary_transaction.objects.get(st_id=request.POST.get('st_id'))
                obj.deductions = float(request.POST['deductions'])
                obj.agp_amount = float(request.POST['agp'])
                obj.da_amount = float(request.POST['da'])
                obj.hra_amount = float(request.POST['hra'])
                obj.ta_amount = float(request.POST['ta'])
                obj.bonus = float(request.POST.get('bonus', 0))
                obj.basic_pay = float(request.POST['basic_pay'])
                obj.approval_status = None
                obj.save()
                messages.success(request, 'Salary transaction updated successfully.')
                return redirect('/staff_salary/')
            except Exception as e:
                messages.error(request, f'Error updating salary transaction: {str(e)}')
                return redirect('/staff_salary/')
        elif 'st_id' in request.GET:
            try:
                data = Salary_transaction.objects.select_related(
                    'staff',
                    'staff__designation',
                    'salary_table'
                ).get(st_id=request.GET.get('st_id'))
                return render(request, 'accountant/edit_salary_transaction.html', {'data': data})
            except Salary_transaction.DoesNotExist:
                messages.error(request, 'Salary transaction not found')
                return redirect('/staff_salary/')
        else:
            return redirect('/staff_salary/')
    else:
        return redirect('/home/')

def salary_transactions_accountant(request):
    if 'accountant' in request.session:
        data = Salary_transaction.objects.filter(
            approval_status='Approved',
            staff_id=request.session['staff_id']
        ).annotate(
            total_salary=F('basic_pay') + F('bonus') + F('da_amount') + 
                        F('hra_amount') + F('ta_amount') + F('agp_amount'),
            payable=F('total_salary') - F('deductions')             
        ).select_related('staff', 'academic_year', 'salary_table')
        return render(request, 'accountant/salary.html', {'data': data})
    else:
        return redirect('/home/')

def new_school_finance_transactions(request):
    if 'accountant' in request.session or 'master' in request.session:
        data = School_finance_transaction.objects.filter(
            Q(approval_status=None) | Q(approval_status='Denied')
        ).select_related('academic_year', 'school_finance')
        
        template = ('master/school_finance_transaction_list.html' 
                   if 'master' in request.session 
                   else 'accountant/school_finance_transaction_list.html')
        
        return render(request, template, {'data': data})
    else:
        return redirect('/home/')

def school_finance_transactions_history(request):
    if 'accountant' in request.session or 'master' in request.session:
        ay = Academic_year.objects.filter(status=True)
        data = School_finance_transaction.objects.filter(
            approval_status='Approved'
        ).select_related('academic_year', 'school_finance')
        
        template = ('master/school_finance_transaction_history.html' 
                   if 'master' in request.session 
                   else 'accountant/school_finance_transaction_history.html')
        
        return render(request, template, {'data': data, 'ay': ay})
    else:
        return redirect('/home/')

def school_finance_transaction_status(request):
    if 'master' in request.session:
        if 'sft_id' in request.GET:
            try:
                obj = School_finance_transaction.objects.get(sft_id=request.GET['sft_id'])
                obj.approval_status = request.GET['status']
                obj.save()
                messages.success(request, 'Status updated successfully.')
                return redirect('/school_finance_transactions_history/')
            except Exception as e:
                messages.error(request, f'Error updating status: {str(e)}')
                return redirect('/new_school_finance_transactions/')
        else:
            return redirect('/new_school_finance_transactions/')
    else:
        return redirect('/home/')

def salary_transaction_details(request, transaction_id):
    if 'master' not in request.session:
        return redirect('/home/')
        
    try:
        # Get transaction with related data
        transaction = Salary_transaction.objects.select_related(
            'staff', 
            'staff__designation',
            'academic_year'
        ).get(st_id=transaction_id)
        
        # Calculate total salary
        total_salary = (
            transaction.basic_pay +
            transaction.da_amount +
            transaction.hra_amount +
            transaction.ta_amount +
            transaction.agp_amount +
            transaction.bonus
        )
        
        # Calculate payable amount
        payable = total_salary - transaction.deductions
        
        # Add calculated fields to transaction object
        transaction.total_salary = total_salary
        transaction.payable = payable
        
        context = {
            'title': 'Salary Transaction Details',
            'transaction': transaction
        }
        
        return render(request, 'master/salary_transaction_details.html', context)
        
    except Salary_transaction.DoesNotExist:
        messages.error(request, 'Transaction not found')
        return redirect('new_salary_transactions')

def admin_leave_status(request):
    if not 'master' in request.session:
        return redirect('/home/')
    
    try:
        if 'sl_id' in request.GET and 'status' in request.GET:
            leave_request = Staff_leave.objects.get(sl_id=request.GET['sl_id'])
            leave_request.status = request.GET['status']
            leave_request.save()
            messages.success(request, f'Leave request has been {request.GET["status"].lower()}')
        else:
            messages.error(request, 'Invalid request parameters')
        return redirect('/new_leave_request/')
    except Staff_leave.DoesNotExist:
        messages.error(request, 'Leave request not found')
        return redirect('/new_leave_request/')
    except Exception as e:
        messages.error(request, f'Error updating leave status: {str(e)}')
        return redirect('/new_leave_request/')

def payment(request):
    if 'student' in request.session:
        # Initialize Razorpay client with credentials from settings
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        if request.method == 'GET':
            try:
                # Get parameters from URL
                sf_id = request.GET.get('sf_id')
                year = request.GET.get('ye')
                month = request.GET.get('mo')
                
                # Validate required parameters
                if not all([sf_id, year, month]):
                    messages.error(request, 'Invalid payment parameters. Please try again from the fee list.')
                    return redirect('fee_list')
                
                # Convert parameters to correct types
                try:
                    sf_id = int(sf_id)
                    year = int(year)
                    month = int(month)
                except (TypeError, ValueError):
                    messages.error(request, 'Invalid parameter values. Please try again from the fee list.')
                    return redirect('fee_list')
                
                # Get required objects
                sf = Student_fee.objects.get(sf_id=sf_id)
                student = Student_register.objects.get(sr_id=request.session['student'])
                ay = Academic_year.objects.get(current_ay=True)
                
                # Check if fee is already paid
                existing_payment = Student_fee_transaction.objects.filter(
                    student_id=request.session['student'],
                    student_fee_id=sf_id,
                    academic_year=ay,
                    payment_date__year=year,
                    payment_date__month=month
                ).exists()
                
                if existing_payment:
                    messages.warning(request, 'This fee has already been paid')
                    return redirect('fee_list')
                
                # Get current date
                current_date = datetime.now().date()
                
                # Calculate due date based on term
                start_year, end_year = map(int, ay.academic_year.split('-'))
                
                # Set due date based on term
                if sf.term == '1':  # First term
                    due_date = date(start_year, 8, 31)  # August 31st
                elif sf.term == '2':  # Second term
                    due_date = date(start_year, 11, 30)  # November 30th
                else:  # Third term
                    due_date = date(end_year, 3, 31)  # March 31st
                
                # Calculate late payment penalty if applicable
                late_fee = 0
                if current_date > due_date:
                    days_late = (current_date - due_date).days
                    late_fee = days_late * 10  # ₹10 per day

                total_amount = sf.amount + late_fee

                # Create Razorpay Order
                razorpay_order = client.order.create({
                    'amount': int(total_amount * 100),  # Amount in paise
                    'currency': 'INR',
                    'payment_capture': '1'
                })
                
                context = {
                    'sf': sf,
                    'student': student,
                    'amount': sf.amount,
                    'late_fee': late_fee,
                    'total_amount': total_amount,
                    'due_date': due_date,
                    'is_late': late_fee > 0,
                    'days_late': (current_date - due_date).days if late_fee > 0 else 0,
                    'razorpay_key': settings.RAZORPAY_KEY_ID,
                    'order_id': razorpay_order['id'],
                    'current_date': current_date
                }
                
                return render(request, 'student/payment.html', context)
                
            except (Student_fee.DoesNotExist, Student_register.DoesNotExist, Academic_year.DoesNotExist) as e:
                messages.error(request, str(e))
                return redirect('fee_list')
            except Exception as e:
                messages.error(request, f'Error processing payment: {str(e)}')
                return redirect('fee_list')
        
        elif request.method == 'POST':
            try:
                payment_id = request.POST.get('razorpay_payment_id')
                order_id = request.POST.get('razorpay_order_id')
                
                if not payment_id or not order_id:
                    messages.error(request, 'Missing payment information')
                    return redirect('fee_list')
                
                # Get parameters from POST data first, then fallback to GET
                sf_id = request.POST.get('sf_id') or request.GET.get('sf_id')
                year = request.POST.get('ye') or request.GET.get('ye')
                month = request.POST.get('mo') or request.GET.get('mo')
                
                # Validate required parameters
                if not all([sf_id, year, month]):
                    messages.error(request, 'Invalid payment parameters. Please try again from the fee list.')
                    return redirect('fee_list')
                
                # Convert parameters to correct types
                try:
                    sf_id = int(sf_id)
                    year = int(year)
                    month = int(month)
                except (TypeError, ValueError):
                    messages.error(request, 'Invalid parameter values. Please try again from the fee list.')
                    return redirect('fee_list')
                
                # Verify the payment signature
                payment = client.payment.fetch(payment_id)
                
                if payment['status'] == 'captured':
                    # Get required objects
                    sf = Student_fee.objects.get(sf_id=sf_id)
                    student = Student_register.objects.get(sr_id=request.session['student'])
                    ay = Academic_year.objects.get(current_ay=True)
                    
                    # Check if payment already exists
                    existing_payment = Student_fee_transaction.objects.filter(
                        student_id=request.session['student'],
                        student_fee_id=sf_id,
                        academic_year=ay,
                        payment_date__year=year,
                        payment_date__month=month
                    ).exists()
                    
                    if existing_payment:
                        messages.warning(request, 'This fee has already been paid')
                        return redirect('fee_list')
                    
                    # Calculate the amount including late fee
                    current_date = datetime.now().date()
                    
                    # Calculate due date
                    start_year, end_year = map(int, ay.academic_year.split('-'))
                    if sf.term == '1':
                        due_date = date(start_year, 8, 31)
                    elif sf.term == '2':
                        due_date = date(start_year, 11, 30)
                    else:
                        due_date = date(end_year, 3, 31)
                    
                    # Calculate late fee if applicable
                    late_fee = 0
                    days_late = 0
                    if current_date > due_date:
                        days_late = (current_date - due_date).days
                        late_fee = days_late * 10
                    
                    total_amount = sf.amount + late_fee
                    
                    # Verify payment amount matches
                    payment_amount = float(payment['amount']) / 100  # Convert from paise to rupees
                    if payment_amount != total_amount:
                        messages.error(request, 'Payment amount mismatch')
                        return redirect('fee_list')
                    
                    # Create transaction record
                    transaction = Student_fee_transaction.objects.create(
                        student=student,
                        academic_year=ay,
                        student_fee=sf,
                        total_amount=total_amount,
                        payment_date=current_date,
                        created_at=current_date,
                        razorpay_payment_id=payment_id,
                        late_payment_days=days_late,
                        late_payment_penalty=late_fee,
                        due_date=due_date
                    )
                    
                    messages.success(request, 'Payment successful! You can download the receipt from the fee list.')
                    return redirect('fee_list')
                else:
                    messages.error(request, f'Payment failed. Status: {payment["status"]}')
                    return redirect('fee_list')
                    
            except (Student_fee.DoesNotExist, Student_register.DoesNotExist, Academic_year.DoesNotExist) as e:
                messages.error(request, f'Error: {str(e)}')
                return redirect('fee_list')
            except Exception as e:
                messages.error(request, f'Error processing payment: {str(e)}')
                return redirect('fee_list')
    
    return redirect('home')

def fee_list(request):
    if 'student' in request.session:
        try:
            student = Student_register.objects.select_related(
                'standard', 
                'standard__educational_level'
            ).get(sr_id=request.session['student'])
            
            current_ay = Academic_year.objects.filter(current_ay=True).first()
            if not current_ay:
                messages.error(request, 'No active academic year found')
                return redirect('home')
            
            # Get current date for payment URL
            current_date = datetime.now().date()
            
            # Parse academic year
            start_year, end_year = map(int, current_ay.academic_year.split('-'))
            
            # Determine current term based on date
            if 6 <= current_date.month <= 8:
                current_term = '1'  # First term (June-August)
            elif 9 <= current_date.month <= 11:
                current_term = '2'  # Second term (September-November)
            else:
                current_term = '3'  # Third term (December-March)

            # Get all fees for student's educational level
            all_fees = Student_fee.objects.filter(
                educational_level=student.standard.educational_level,
                status=True
            ).order_by('term', 'fee_type')

            # Get paid fees for lookup
            paid_fees = Student_fee_transaction.objects.filter(
                student_id=student.sr_id,
                academic_year=current_ay
            ).values('student_fee_id', 'sft_id', 'payment_date', 'late_payment_penalty')

            # Create lookup dictionary for paid fees
            paid_fee_lookup = {
                payment['student_fee_id']: {
                    'sft_id': payment['sft_id'],
                    'payment_date': payment['payment_date'],
                    'late_penalty': payment['late_payment_penalty']
                }
                for payment in paid_fees
            }

            # Process fees and add payment status
            fee_data = []
            total_late_fees = 0
            
            for fee in all_fees:
                # Calculate due date based on term
                if fee.term == '1':
                    due_date = date(start_year, 8, 31)  # August 31st
                elif fee.term == '2':
                    due_date = date(start_year, 11, 30)  # November 30th
                else:
                    due_date = date(end_year, 3, 31)  # March 31st

                # Check if fee is paid
                payment_info = paid_fee_lookup.get(fee.sf_id)
                is_paid = payment_info is not None
                is_overdue = not is_paid and current_date > due_date

                # Calculate late fee if overdue
                days_late = 0
                late_fee = 0
                total_with_fine = fee.amount

                if is_overdue:
                    days_late = (current_date - due_date).days
                    late_fee = days_late * 10  # ₹10 per day
                    total_with_fine = fee.amount + late_fee
                    total_late_fees += late_fee
                elif is_paid and payment_info['late_penalty'] > 0:
                    late_fee = payment_info['late_penalty']
                    payment_date = payment_info['payment_date']
                    days_late = (payment_date - due_date).days
                    total_late_fees += late_fee

                fee_data.append({
                    'sf_id': fee.sf_id,
                    'fee_type': fee.fee_type,
                    'educational_level': fee.educational_level.level,
                    'amount': fee.amount,
                    'term': str(fee.term),
                    'due_date': due_date.strftime('%d %B %Y'),
                    'paid': is_paid,
                    'is_overdue': is_overdue,
                    'days_late': days_late,
                    'late_fee': late_fee,
                    'total_with_fine': total_with_fine,
                    'transaction_id': payment_info['sft_id'] if is_paid else None,
                    'term_name': {
                        '1': 'First Term (June-August)',
                        '2': 'Second Term (September-November)',
                        '3': 'Third Term (December-March)'
                    }.get(str(fee.term)),
                    'paid_late': is_paid and payment_info['late_penalty'] > 0,
                    'late_fee_paid': payment_info['late_penalty'] if is_paid else 0
                })

            # Calculate totals
            total_fees = sum(fee['amount'] for fee in fee_data)
            total_with_penalties = total_fees + total_late_fees

            context = {
                'fee_data': fee_data,
                'student': student,
                'current_term': str(current_term),
                'academic_year': current_ay,
                'academic_year_start': f"June {start_year}",
                'academic_year_end': f"April {end_year}",
                'total_fees': total_fees,
                'total_late_fees': total_late_fees,
                'total_with_penalties': total_with_penalties,
                'current_date': current_date
            }
            
            return render(request, 'student/fee_list.html', context)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')
    return redirect('home')

def fee_payment(request):
    if 'student' in request.session:
        student = Student_register.objects.get(sr_id=request.session['student'])
        ay = Academic_year.objects.filter(current_ay=True).first()
        
        if not ay:
            return render(request, 'student/fee_payment.html', {'data': None, 'ay': None})
            
        if request.GET.get('sf_id'):
            try:
                sf = Student_fee.objects.get(sf_id=request.GET['sf_id'])
                
                # Parse academic year
                start_year, end_year = map(int, ay.academic_year.split('-'))
                
                # Get current date
                current_date = datetime.now()
                
                # Get all payments for this fee
                paid_months = Student_fee_transaction.objects.filter(
                    student_id=student.sr_id,
                    student_fee=sf,
                    academic_year=ay
                ).values_list('payment_date__year', 'payment_date__month')
                
                # Create lookup for paid months
                paid_lookup = {f"{year}-{month}" for year, month in paid_months}
                
                # Generate monthly data
                monthly_data = []
                
                # First part (June to December)
                if current_date.year == start_year:
                    # Show months from June to current month only
                    for month in range(6, current_date.month + 1):
                        month_key = f"{start_year}-{month}"
                        is_paid = month_key in paid_lookup
                        due_date = date(start_year, month + 1, 15)
                        is_overdue = not is_paid and current_date.date() > due_date
                        
                        monthly_data.append({
                            'month': month,
                            'year': start_year,
                            'status': is_paid,
                            'total': sf.amount,
                            'fine': 100 if is_overdue else 0,
                            'month_name': date(start_year, month, 1).strftime('%B %Y')
                        })
                
                # Second part (January to April)
                elif current_date.year == end_year and current_date.month <= 4:
                    # Show all months from June to December of previous year
                    for month in range(6, 13):
                        month_key = f"{start_year}-{month}"
                        is_paid = month_key in paid_lookup
                        due_date = date(start_year, month + 1, 15)
                        is_overdue = not is_paid and current_date.date() > due_date
                        
                        monthly_data.append({
                            'month': month,
                            'year': start_year,
                            'status': is_paid,
                            'total': sf.amount,
                            'fine': 100 if is_overdue else 0,
                            'month_name': date(start_year, month, 1).strftime('%B %Y')
                        })
                    
                    # Add months from January to current month
                    for month in range(1, current_date.month + 1):
                        month_key = f"{end_year}-{month}"
                        is_paid = month_key in paid_lookup
                        due_date = date(end_year, month + 1, 15)
                        is_overdue = not is_paid and current_date.date() > due_date
                        
                        monthly_data.append({
                            'month': month,
                            'year': end_year,
                            'status': is_paid,
                            'total': sf.amount,
                            'fine': 100 if is_overdue else 0,
                            'month_name': date(end_year, month, 1).strftime('%B %Y')
                        })
                
                return render(request, 'student/fee_payment.html', {
                    'fee': sf,
                    'ay': ay,
                    'sf_id': sf.sf_id,
                    'data': monthly_data
                })
                
            except Student_fee.DoesNotExist:
                messages.error(request, 'Fee type not found')
                return redirect('fee_list')
                
        return render(request, 'student/fee_payment.html', {'data': 'Not exist'})
    return redirect('/home/')

def promotion_history(request):
    if 'master' in request.session or 'accountant' in request.session:
        promotions = StudentPromotion.objects.select_related(
            'student',
            'from_standard',
            'to_standard',
            'academic_year'
        ).order_by('-promotion_date')
        
        template = 'master/promotion_history.html' if 'master' in request.session else 'accountant/promotion_history.html'
        
        return render(request, template, {
            'promotions': promotions,
            'title': 'Student Promotion History'
        })
    return redirect('/home/')

def fee_receipt(request, transaction_id):
    if 'student' in request.session:
        try:
            transaction = Student_fee_transaction.objects.select_related(
                'student',
                'student_fee',
                'academic_year',
                'student__standard',
                'student__standard__educational_level'
            ).get(sft_id=transaction_id, student_id=request.session['student'])
            
            context = {
                'transaction': transaction,
                'payment_date': transaction.payment_date,
                'created_at': transaction.created_at,
                'receipt_no': f"FEE/{transaction.sft_id}/{transaction.payment_date.year}",
                'student_name': transaction.student.name,
                'student': transaction.student,  # Add this line
                'fee_type': transaction.student_fee.fee_type,
                'amount': transaction.total_amount,
                'academic_year': transaction.academic_year.academic_year
            }
            
            template = get_template('student/fee_receipt_pdf.html')
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="fee_receipt_{transaction.sft_id}.pdf"'
            
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('PDF generation error')
            return response
            
        except Student_fee_transaction.DoesNotExist:
            messages.error(request, 'Transaction not found')
            return redirect('fee_list')
        except Exception as e:
            messages.error(request, f'Error generating receipt: {str(e)}')
            return redirect('fee_list')
    return redirect('home')

def paid_fees(request):
    if 'student' in request.session:
        try:
            student = Student_register.objects.select_related(
                'standard', 
                'standard__educational_level'
            ).get(sr_id=request.session['student'])
            
            current_ay = Academic_year.objects.filter(current_ay=True).first()
            if not current_ay:
                messages.error(request, 'No active academic year found')
                return redirect('home')
            
            # Get all paid fees for the student
            paid_transactions = Student_fee_transaction.objects.select_related(
                'student_fee',
                'academic_year'
            ).filter(
                student=student,
                academic_year=current_ay
            ).order_by('-payment_date')
            
            context = {
                'transactions': paid_transactions,
                'student': student,
                'academic_year': current_ay
            }
            
            return render(request, 'student/paid_fees.html', context)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('home')
    return redirect('home')

def check_and_update_academic_year():
    """
    Check and update academic year based on current date.
    Academic year runs from June 1st to May 31st of the following year.
    Automatically shifts to next academic year on June 1st.
    """
    current_date = timezone.now().date()
    current_month = current_date.month
    current_year = current_date.year

    # Determine academic year based on current date
    if current_month >= 6:  # June to December
        start_year = current_year
    else:  # January to May
        start_year = current_year - 1
    end_year = start_year + 1

    academic_year = f"{start_year}-{end_year}"
    start_date = date(start_year, 6, 1)
    end_date = date(end_year, 5, 31)

    try:
        # Get or create the current academic year
        ay, created = Academic_year.objects.get_or_create(
            academic_year=academic_year,
            defaults={
                'start_date': start_date,
                'end_date': end_date,
                'current_ay': True,
                'status': True
            }
        )

        # If the academic year exists but dates aren't set, update them
        if not created and (ay.start_date is None or ay.end_date is None):
            ay.start_date = start_date
            ay.end_date = end_date
            ay.save()

        # If it's June 1st or later and we haven't updated the current academic year
        if current_date >= start_date and not ay.current_ay:
            # Update current academic year
            Academic_year.objects.all().update(current_ay=False)
            ay.current_ay = True
            ay.save()

            # Handle student promotions on June 1st
            if current_date.month == 6 and current_date.day == 1:
                promote_students(ay)

        # Create next academic year 2 months before current year ends
        next_ay_start = date(end_year, 6, 1)
        if (next_ay_start - current_date).days <= 60:
            next_academic_year = f"{end_year}-{end_year + 1}"
            next_ay, created = Academic_year.objects.get_or_create(
                academic_year=next_academic_year,
                defaults={
                    'start_date': next_ay_start,
                    'end_date': date(end_year + 1, 5, 31),
                    'current_ay': False,
                    'status': True
                }
            )
            
            # If next academic year exists but dates aren't set, update them
            if not created and (next_ay.start_date is None or next_ay.end_date is None):
                next_ay.start_date = next_ay_start
                next_ay.end_date = date(end_year + 1, 5, 31)
                next_ay.save()

    except Exception as e:
        print(f"Error updating academic year: {str(e)}")

def promote_students(new_academic_year):
    """Handle student promotions to next standard/educational level"""
    students = Student_register.objects.select_related(
        'standard', 
        'standard__educational_level'
    ).all()

    for student in students:
        if student.standard:
            try:
                # Try to get next standard in same educational level
                next_standard = Standard.objects.get(
                    educational_level=student.standard.educational_level,
                    standard=student.standard.standard + 1
                )
            except Standard.DoesNotExist:
                # Try to get first standard of next educational level
                try:
                    next_el = Educational_level.objects.filter(
                        el_id__gt=student.standard.educational_level.el_id
                    ).order_by('el_id').first()
                    
                    if next_el:
                        next_standard = Standard.objects.filter(
                            educational_level=next_el
                        ).order_by('standard').first()
                    else:
                        continue  # Skip if no next level exists
                except Exception:
                    continue  # Skip if any error occurs
            
            if next_standard:
                # Create promotion record
                StudentPromotion.objects.create(
                    student=student,
                    from_standard=student.standard,
                    to_standard=next_standard,
                    academic_year=new_academic_year
                )
                
                # Update student's standard
                student.standard = next_standard
                student.save()

def check_session(request):
    """Check if the user session is still valid"""
    is_valid = 'login_id' in request.session
    return JsonResponse({'valid': is_valid})

def master_student_fee(request):
    if 'master' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        account_category = request.POST.get('account_category')
        educational_level_id = request.POST.get('educational_level_id')
        fee_type = request.POST.get('fee_type')
        amount = request.POST.get('amount')
        
        try:
            educational_level = EducationalLevel.objects.get(el_id=educational_level_id)
            StudentFee.objects.create(
                account_category=account_category,
                educational_level=educational_level,
                fee_type=fee_type,
                amount=amount,
                status=True
            )
            messages.success(request, 'Fee structure added successfully!')
            return redirect('master_student_fee')
        except Exception as e:
            messages.error(request, f'Error adding fee structure: {str(e)}')
    
    context = {
        'edl': EducationalLevel.objects.filter(status=True),
        'data': StudentFee.objects.select_related('educational_level').all().order_by('-sf_id')
    }
    return render(request, 'master/student_fee.html', context)

def master_edit_student_fee(request):
    if 'master' not in request.session:
        return redirect('login')
    
    fee_id = request.GET.get('id')
    try:
        fee = StudentFee.objects.get(sf_id=fee_id)
        if request.method == 'POST':
            fee.account_category = request.POST.get('account_category')
            fee.educational_level_id = request.POST.get('educational_level_id')
            fee.fee_type = request.POST.get('fee_type')
            fee.amount = request.POST.get('amount')
            fee.save()
            messages.success(request, 'Fee structure updated successfully!')
            return redirect('master_student_fee')
        
        context = {
            'fee': fee,
            'edl': EducationalLevel.objects.filter(status=True)
        }
        return render(request, 'master/edit_student_fee.html', context)
    except StudentFee.DoesNotExist:
        messages.error(request, 'Fee structure not found!')
        return redirect('master_student_fee')

def master_status_student_fee(request):
    if 'master' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        fee_id = request.POST.get('id')
        try:
            fee = StudentFee.objects.get(sf_id=fee_id)
            fee.status = not fee.status
            fee.save()
            return JsonResponse({'status': 'success'})
        except StudentFee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Fee not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def master_check_student_fee_exist(request):
    if 'master' not in request.session:
        return JsonResponse({'exists': True})
    
    educational_level_id = request.GET.get('educational_level_id')
    fee_type = request.GET.get('fee_type')
    
    exists = StudentFee.objects.filter(
        educational_level_id=educational_level_id,
        fee_type__iexact=fee_type
    ).exists()
    
    return JsonResponse({'exists': exists})

@never_cache
def staff_attendance(request):
    if 'master' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    try:
        current_ay = Academic_year.objects.get(current_ay=True)
        
        # Get selected date from request or use current date
        selected_date = request.GET.get('attendance_date') or request.POST.get('attendance_date')
        if selected_date:
            try:
                selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            except ValueError:
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()
            
        # Get all active staff
        staff_list = Staff_register.objects.select_related('designation').filter(login__status=True)
        
        # Get existing attendance records
        attendance_records = {}
        leave_status = {}  # Add this to track leave status
        
        if selected_date:
            # Get attendance records
            records = StaffAttendance.objects.filter(
                attendance_date=selected_date,
                academic_year=current_ay
            ).select_related('attendance_status', 'staff')
            
            attendance_records = {
                str(record.staff.sr_id): 'present' if record.attendance_status.status_name == 'Present' else 'absent'
                for record in records
            }
            
            # Get leave status for all staff
            for staff in staff_list:
                has_leave = Staff_leave.objects.filter(
                    staff_id=staff.sr_id,
                    start_date__lte=selected_date,
                    end_date__gte=selected_date,
                    status='Approved',
                    academic_year=current_ay
                ).exists()
                leave_status[str(staff.sr_id)] = has_leave

        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'attendance_records': attendance_records,
                'leave_status': leave_status,
                'selected_date': selected_date.strftime('%Y-%m-%d'),
            })

        context = {
            'staff_list': staff_list,
            'selected_date': selected_date,
            'attendance_records': attendance_records,
            'min_date': current_ay.start_date,
        }

        return render(request, 'master/staff_attendance.html', context)

    except Exception as e:
        import traceback
        print("Error in staff_attendance:", str(e))
        print(traceback.format_exc())
        messages.error(request, f'Error: {str(e)}')
        return redirect('master_home')

def view_staff_attendance(request):
    if 'master' not in request.session:
        return redirect('login')
    
    current_ay = Academic_year.objects.get(current_ay=True)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_staff_id = request.GET.get('staff_id')
    
    staff_list = Staff_register.objects.select_related('designation').all()
    attendance_data = []
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        staff_query = staff_list
        if selected_staff_id:
            staff_query = staff_list.filter(sr_id=selected_staff_id)
        
        for staff in staff_query:
            attendance_records = []
            current_date = start_date
            
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Skip weekends
                    try:
                        record = StaffAttendance.objects.get(
                            staff=staff,
                            attendance_date=current_date,
                            academic_year=current_ay
                        )
                        status = record.attendance_status.status_name
                    except StaffAttendance.DoesNotExist:
                        status = None
                    
                    attendance_records.append({
                        'date': current_date,
                        'status': status
                    })
                current_date += timedelta(days=1)
            
            if attendance_records:  # Only add staff with attendance records
                attendance_data.append({
                    'staff': staff,
                    'attendance': attendance_records
                })
    
    context = {
        'staff_list': staff_list,
        'attendance_data': attendance_data,
        'start_date': start_date if start_date else '',
        'end_date': end_date if end_date else '',
        'selected_staff_id': selected_staff_id,
        'min_date': current_ay.start_date,
        'max_date': current_ay.end_date
    }
    return render(request, 'master/view_staff_attendance.html', context)

def check_leave_availability(request):
    try:
        start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
        leave_type = Leave_type.objects.get(lt_id=request.GET['leave_type_id'])
        
        # Calculate working days
        no_of_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Skip weekends
                no_of_days += 1
            current_date += timedelta(days=1)
            
        # Get staff ID
        staff_id = None
        if 'accountant' in request.session:
            staff_id = request.session['accountant']
        elif 'office_staff' in request.session:
            staff_id = request.session['office_staff']
        elif 'faculty' in request.session:
            staff_id = request.session['faculty']
            
        if not staff_id:
            return JsonResponse({'available': False, 'message': 'Invalid staff member'})
            
        # Check for overlapping leaves
        if Staff_leave.objects.filter(
            staff_id=staff_id,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists():
            return JsonResponse({
                'available': False,
                'message': 'You already have leave scheduled for these dates'
            })
            
        # Check monthly limit
        month_start = start_date.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        month_end = next_month - timedelta(days=1)
        
        monthly_leaves = Staff_leave.objects.filter(
            staff_id=staff_id,
            leave_type=leave_type,
            start_date__gte=month_start,
            end_date__lte=month_end,
            status='Approved'
        ).aggregate(total_days=Sum('no_of_days'))['total_days'] or 0
        
        if monthly_leaves + no_of_days > leave_type.max_days_per_month:
            return JsonResponse({
                'available': False,
                'message': f'Cannot take more than {leave_type.max_days_per_month} {leave_type.leave_type} days in a month'
            })
            
        # Check yearly limit
        current_ay = Academic_year.objects.get(current_ay=True)
        yearly_leaves = Staff_leave.objects.filter(
            staff_id=staff_id,
            leave_type=leave_type,
            academic_year=current_ay,
            status='Approved'
        ).aggregate(total_days=Sum('no_of_days'))['total_days'] or 0
        
        if yearly_leaves + no_of_days > leave_type.days:
            return JsonResponse({
                'available': False,
                'message': f'Cannot take more than {leave_type.days} {leave_type.leave_type} days in an academic year'
            })
            
        return JsonResponse({'available': True})
        
    except Exception as e:
        return JsonResponse({'available': False, 'message': str(e)})

def process_salary_payment(request):
    if request.method != 'POST' or 'accountant' not in request.session:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request'
        }, status=400)

    try:
        # Get salary transaction
        salary_id = request.POST.get('salary_id')
        salary = Salary_transaction.objects.get(st_id=salary_id)

        # Verify it's approved and not paid
        if salary.approval_status != 'Approved':
            raise ValueError('Salary must be approved before payment')
        if salary.payment_status:
            raise ValueError('Salary has already been paid')

        # Process payment
        salary.payment_status = True
        salary.payment_date = timezone.now()
        salary.payment_method = request.POST.get('payment_method')
        salary.payment_transaction_id = request.POST.get('transaction_ref')
        salary.save()

        # Record the expense
        School_finance_transaction.objects.create(
            academic_year=salary.academic_year,
            school_finance=School_finance.objects.get(
                account_category='Expense',
                finance_type='Staff Salary'
            ),
            description=f'Salary payment for {salary.staff.name} - {salary.salary_date.strftime("%B %Y")}',
            total_amount=salary.payable,
            entry_date=timezone.now(),
            approval_status='Approved'
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Payment processed successfully'
        })

    except Salary_transaction.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Salary transaction not found'
        }, status=404)
    except ValueError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        print(f"Error processing salary payment: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Error processing payment'
        }, status=500)