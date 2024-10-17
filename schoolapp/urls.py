"""
URL configuration for School_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index,name="index"),
    path('index/', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('login/', views.login,name="login"),
    path('contact/', views.contact,name="contact"),
    path('home/', views.home,name="home"),

    path('master_home/', views.master_home,name="master_home"),
    path('accountant_home/', views.accountant_home,name="accountant_home"),
    path('office_staff_home/', views.office_staff_home,name="office_staff_home"),
    path('faculty_home/', views.faculty_home,name="faculty_home"),
    path('student_home/', views.student_home,name="student_home"),

    path('designation/', views.designation,name="designation"),
    path('edit_designation/', views.edit_designation,name="edit_designation"),
    path('status_designation/', views.status_designation,name="status_designation"),

    path('academic_year/', views.academic_year,name="academic_year"),
    path('edit_academic_year/', views.edit_academic_year,name="edit_academic_year"),
    path('status_academic_year/', views.status_academic_year,name="status_academic_year"),

    path('leave_type/', views.leave_type,name="leave_type"),
    path('edit_leave_type/', views.edit_leave_type,name="edit_leave_type"),
    path('status_leave_type/', views.status_leave_type,name="status_leave_type"),

    path('staff_register/', views.staff_register,name="staff_register"),
    path('staff_list/', views.staff_list,name="staff_list"),
    path('student_register/', views.student_register,name="student_register"),

    path('school_finance/', views.school_finance,name="school_finance"),
    path('edit_school_finance/', views.edit_school_finance,name="edit_school_finance"),
    path('status_school_finance/', views.status_school_finance,name="status_school_finance"),
    path('salary_table/', views.salary_table,name="salary_table"),
    path('edit_salary_table/', views.edit_salary_table,name="edit_salary_table"),
    path('status_salary_table/', views.status_salary_table,name="status_salary_table"),
    path('student_fee/', views.student_fee,name="student_fee"),
    path('edit_student_fee/', views.edit_student_fee,name="edit_student_fee"),
    path('status_student_fee/', views.status_student_fee,name="status_student_fee"),

    path('leave_apply/', views.leave_apply,name="leave_apply"),
    path('leave_list/', views.leave_list,name="leave_list"),
    path('new_leave_request/', views.new_leave_request,name="new_leave_request"),
    path('leave_status/', views.leave_status,name="leave_status"),
    path('check_leave_exist/', views.check_leave_exist,name="check_leave_exist"),

    path('staff_salary/', views.staff_salary,name="staff_salary"),
    path('search_staff_salary/', views.search_staff_salary,name="search_staff_salary"),
    path('salary_transaction/', views.salary_transaction,name="salary_transaction"),
    path('school_finance_transaction/', views.school_finance_transaction,name="school_finance_transaction"),
    path('new_salary_transactions/', views.new_salary_transactions,name="new_salary_transactions"),
    path('salary_transactions_history/', views.salary_transactions_history,name="salary_transactions_history"),
    path('salary_transactions_status/', views.salary_transactions_status,name="salary_transactions_status"),
    path('salary_details/', views.salary_details,name="salary_details"),
    path('new_school_finance_transactions/', views.new_school_finance_transactions,name="new_school_finance_transactions"),
    path('school_finance_transactions_history/', views.school_finance_transactions_history,name="school_finance_transactions_history"),
    path('school_finance_transaction_status/', views.school_finance_transaction_status,name="school_finance_transaction_status"),

    path('profile/', views.profile,name="profile"),

    path('check_value_exist/', views.check_value_exist,name="check_value_exist"),
    path('check_academic_year_exist/', views.check_academic_year_exist,name="check_academic_year_exist"),
    path('sign_out/', views.sign_out,name="sign_out"),
    path('check_username/', views.check_username,name="check_username"),
    path('check_email/', views.check_email,name="check_email"),
 
    path('master_reg/', views.master_reg,name="master_reg"),
]