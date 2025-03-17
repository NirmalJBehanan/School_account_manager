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
    path('', views.index,name="home"),
    path('index/', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('login/', views.login,name="login"),
    path('contact/', views.contact,name="contact"),
    path('home/', views.home,name="home"),
    path('check_session/', views.check_session, name='check_session'),

    path('master_home/', views.master_home,name="master_home"),
    path('accountant_home/', views.accountant_home,name="accountant_home"),
    path('office_staff_home/', views.office_staff_home,name="office_staff_home"),
    path('faculty_home/', views.faculty_home,name="faculty_home"),
    path('student_home/', views.student_home,name="student_home"),

    path('designation/', views.designation,name="designation"),
    path('edit_designation/', views.edit_designation,name="edit_designation"),
    path('status_designation/', views.status_designation,name="status_designation"),

    path('academic_year/', views.academic_year,name="academic_year"),
    path('update_current_ay/', views.update_current_ay,name="update_current_ay"),

    path('leave_type/', views.leave_type,name="leave_type"),
    path('edit_leave_type/', views.edit_leave_type,name="edit_leave_type"),
    path('status_leave_type/', views.status_leave_type,name="status_leave_type"),

    path('staff_register/', views.staff_register,name="staff_register"),
    path('staff_list/', views.staff_list,name="staff_list"),
    path('staff_status/', views.staff_status,name="staff_status"),
    path('student_register/', views.student_register,name="student_register"),
    path('student_list/', views.student_list,name="student_list"),
    path('student_status/', views.student_status, name='student_status'),

    path('school_finance/', views.school_finance, name='school_finance'),
    path('edit_school_finance/', views.edit_school_finance,name="edit_school_finance"),
    path('status_school_finance/', views.status_school_finance,name="status_school_finance"),
    path('salary_table/', views.salary_table, name='salary_table'),
    path('edit_salary_table/', views.edit_salary_table,name="edit_salary_table"),
    path('status_salary_table/', views.status_salary_table,name="status_salary_table"),

    path('leave_apply/', views.leave_apply,name="leave_apply"),
    path('leave_list/', views.leave_list, name='leave_list'),
    path('new_leave_request/', views.new_leave_request,name="new_leave_request"),
    path('admin_leave_status/', views.admin_leave_status, name="admin_leave_status"),
    path('leave_status/', views.leave_status,name="leave_status"),
    path('check_leave_exist/', views.check_leave_exist,name="check_leave_exist"),

    path('staff_salary/', views.staff_salary,name="staff_salary"),
    path('search_staff_salary/', views.search_staff_salary,name="search_staff_salary"),
    path('salary_transaction/', views.salary_transaction, name='salary_transaction'),
    path('edit_salary_transaction/', views.edit_salary_transaction,name="edit_salary_transaction"),
    path('edit_finance_transaction/', views.edit_finance_transaction,name="edit_finance_transaction"),

    path('school_finance_transaction/', views.school_finance_transaction,name="school_finance_transaction"),
    path('new_salary_transactions/', views.new_salary_transactions, name='new_salary_transactions'),
    path('salary_transactions_history/', views.salary_transactions_history, name='salary_transactions_history'),
    path('salary_transactions_status/', views.salary_transactions_status, name='salary_transactions_status'),
    path('salary_details/', views.salary_details, name='salary_details'),
    path('salary_transactions_accountant/', views.salary_transactions_accountant,name="salary_transactions_accountant"),
    
    path('new_school_finance_transactions/', views.new_school_finance_transactions,name="new_school_finance_transactions"),
    path('school_finance_transactions_history/', views.school_finance_transactions_history,name="school_finance_transactions_history"),
    path('school_finance_transaction_status/', views.school_finance_transaction_status,name="school_finance_transaction_status"),
    path('payment/', views.payment,name="payment"),
    path('student_fee_transactions/', views.student_fee_transactions, name='student_fee_transactions'),
    path('salary_pdf/', views.salary_pdf,name="salary_pdf"),
    path('school_finance_pdf/', views.school_finance_pdf,name="school_finance_pdf"),
    path('student_fee_pdf/', views.student_fee_pdf,name="student_fee_pdf"),
    path('student_fee_dues/', views.student_fee_dues,name="student_fee_dues"),
    path('salary_slip/', views.salary_slip,name="salary_slip"),
    path('fee_pdf/', views.fee_pdf,name="fee_pdf"),

    path('school_transactions/', views.school_transactions,name="school_transactions"),
    path('school_transactions_search/', views.school_transactions_search,name="school_transactions_search"),
    path('school_transactions_pdf/', views.school_transactions_pdf,name="school_transactions_pdf"),
    
    path('search_salary/', views.search_salary,name="search_salary"),
    path('search_school_finance/', views.search_school_finance,name="search_school_finance"),
    path('search_student_fee/', views.search_student_fee,name="search_student_fee"),

    path('search_student/', views.search_student,name="search_student"),
    path('profile/', views.profile,name="profile"),

    path('check_value_exist/', views.check_value_exist,name="check_value_exist"),
    path('check_value_exist2/', views.check_value_exist2,name="check_value_exist2"),
    path('check_academic_year_exist/', views.check_academic_year_exist,name="check_academic_year_exist"),
    path('sign_out/', views.sign_out,name="sign_out"),
    path('check_username/', views.check_username,name="check_username"),
    path('check_email/', views.check_email,name="check_email"),
 
    path('master_reg/', views.master_reg,name="master_reg"),
    path('blockchain_view/', views.blockchain_view, name='blockchain_view'),
    path('salary-transaction/<int:transaction_id>/', views.salary_transaction_details, name='salary_transaction_details'),
    path('fee_list/', views.fee_list, name='fee_list'),
    path('fee_payment/', views.fee_payment, name='fee_payment'),
    path('promotion_history/', views.promotion_history, name='promotion_history'),
    path('fee_receipt/<int:transaction_id>/', views.fee_receipt, name='fee_receipt'),
    path('paid_fees/', views.paid_fees, name='paid_fees'),

    # Student Fee Management URLs
    path('student_fee/', views.student_fee, name='student_fee'),
    path('edit_student_fee/', views.edit_student_fee, name='edit_student_fee'),
    path('status_student_fee/', views.status_student_fee, name='status_student_fee'),
    path('check_student_fee_exist/', views.check_student_fee_exist, name='check_student_fee_exist'),
    path('get_fee_limits/', views.get_fee_limits, name='get_fee_limits'),

    # Attendance Management URLs
    path('staff_attendance/', views.staff_attendance, name='staff_attendance'),
    path('view_staff_attendance/', views.view_staff_attendance, name='view_staff_attendance'),

    path('check_leave_availability/', views.check_leave_availability, name='check_leave_availability'),

    path('process_salary_payment/', views.process_salary_payment, name='process_salary_payment'),
]