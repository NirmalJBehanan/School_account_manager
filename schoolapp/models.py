from django.db import models
from django.utils import timezone

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.TextField()
    user_type = models.CharField(max_length=15)
    status = models.CharField(max_length=15,null=True)
    class Meta:
        db_table = 'Login'

class Educational_level(models.Model):
    el_id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=25)
    class Meta: 
        db_table = 'Educational_level'
    
class Standard(models.Model):
    s_id = models.AutoField(primary_key=True)
    educational_level = models.ForeignKey(Educational_level,on_delete=models.CASCADE)
    standard = models.IntegerField()
    class Meta:
        db_table = 'Standard'
   
class Academic_year(models.Model):
    ay_id = models.AutoField(primary_key=True)
    academic_year = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Academic_year'

class Designation(models.Model):
    d_id = models.AutoField(primary_key=True)
    designation_name = models.CharField(max_length=40)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Designation'

class Leave_type(models.Model):
    lt_id = models.AutoField(primary_key=True)
    leave_type = models.CharField(max_length=60)
    days = models.IntegerField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Leave_type'

class Staff_register(models.Model):
    sr_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login,on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=80,null=True)
    contact_number = models.BigIntegerField(null=True)
    address = models.TextField(null=True)  
    image = models.TextField(null=True) 
    class Meta:
        db_table = 'Staff_register'
    
class Student_register(models.Model):
    sr_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login,on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=80, null=True)
    email = models.CharField(max_length=40)
    contact_number = models.BigIntegerField()
    address = models.TextField()  
    image = models.TextField()  
    gender = models.CharField(max_length=10)
    class Meta:
        db_table = 'Student_register'
    
    
class Salary_table(models.Model):
    st_id = models.AutoField(primary_key=True)
    account_category = models.CharField(max_length=20)
    designation = models.ForeignKey(Designation,on_delete=models.CASCADE)
    basic_pay = models.IntegerField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Salary_table'

class Student_fee(models.Model):
    sf_id = models.AutoField(primary_key=True)
    educational_level = models.ForeignKey(Educational_level,on_delete=models.CASCADE)
    account_category = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=150)
    amount = models.FloatField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Student_fee'

class School_finance(models.Model):
    sf_id = models.AutoField(primary_key=True)
    account_category = models.CharField(max_length=20)
    finance_type = models.CharField(max_length=40)
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'School_finance'

class Salary_transaction(models.Model):
    st_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff_register,on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Academic_year,on_delete=models.SET_NULL,null=True)
    salary_table = models.ForeignKey(Salary_table,on_delete=models.SET_NULL,null=True)
    bonus = models.FloatField(default=0,null=True)
    deductions = models.FloatField(default=0,null=True)
    arrear = models.FloatField(default=0,null=True)
    advance = models.FloatField(default=0,null=True)
    da = models.FloatField(default=0,null=True)
    hra = models.FloatField(default=0,null=True)
    ta = models.FloatField(default=0,null=True)
    agp = models.FloatField(default=0,null=True)
    basic_pay = models.FloatField()
    salary_date = models.DateField()
    approval_status = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'Salary_transaction'

class Student_fee_transaction(models.Model):
    sft_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_register,on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Academic_year,on_delete=models.SET_NULL,null=True)
    student_fee = models.ForeignKey(Student_fee,on_delete=models.SET_NULL,null=True)
    total_amount = models.FloatField()
    payment_date = models.DateField()
    class Meta:
        db_table = 'Student_fee_transaction'

class School_finance_transaction(models.Model):
    sft_id = models.AutoField(primary_key=True)
    academic_year = models.ForeignKey(Academic_year,on_delete=models.SET_NULL,null=True)
    school_finance = models.ForeignKey(School_finance,on_delete=models.SET_NULL,null=True)
    description = models.TextField()
    total_amount = models.FloatField()
    entry_date = models.DateField()
    approval_status = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'School_finance_transaction'

class Staff_leave(models.Model):
    sl_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff_register,on_delete=models.CASCADE)
    leave_type = models.ForeignKey(Leave_type,on_delete=models.SET_NULL,null=True)
    reason = models.TextField() 
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20,null=True)
    class Meta:
            db_table = 'Staff_leave'