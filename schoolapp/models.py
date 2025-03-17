from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core import validators

class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    password = models.TextField()
    user_type = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
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
    academic_year = models.CharField(max_length=25)  # Format: "YYYY-YYYY"
    start_date = models.DateField(null=True)  # June 1st of start year
    end_date = models.DateField(null=True)    # May 31st of end year
    current_ay = models.BooleanField(default=False)
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
    LEAVE_CHOICES = [
        ('casual', 'Casual Leave'),
        ('vacation', 'Vacation Leave')
    ]
    
    lt_id = models.AutoField(primary_key=True)
    leave_type = models.CharField(
        max_length=60, 
        choices=LEAVE_CHOICES, 
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^(casual|vacation)$',
                message='Only Casual Leave and Vacation Leave are allowed',
                code='invalid_leave_type'
            )
        ]
    )
    days = models.IntegerField()
    max_days_per_month = models.IntegerField(default=5)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'Leave_type'

    def save(self, *args, **kwargs):
        # Force the correct values based on leave type
        if self.leave_type == 'casual':
            self.days = 15
            self.max_days_per_month = 5
        elif self.leave_type == 'vacation':
            self.days = 30
            self.max_days_per_month = 5
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of casual and vacation leave types
        if self.leave_type in ['casual', 'vacation']:
            raise ValidationError(f"Cannot delete {self.get_leave_type_display()}")
        super().delete(*args, **kwargs)

class Staff_register(models.Model):
    sr_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login,on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=150,null=True)
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
    da = models.FloatField()
    hra = models.FloatField()
    ta = models.FloatField()
    agp = models.FloatField()
    status = models.BooleanField(default=True)
    class Meta:
        db_table = 'Salary_table'

class Student_fee(models.Model):
    TERM_CHOICES = [
        ('1', 'First Term (June-August)'),
        ('2', 'Second Term (September-November)'),
        ('3', 'Third Term (December-March)')
    ]
    
    sf_id = models.AutoField(primary_key=True)
    educational_level = models.ForeignKey(Educational_level, on_delete=models.CASCADE)
    account_category = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=150)
    amount = models.FloatField()
    term = models.CharField(max_length=1, choices=TERM_CHOICES)
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'Student_fee'

class FeeLimit(models.Model):
    fl_id = models.AutoField(primary_key=True)
    educational_level = models.ForeignKey(Educational_level, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=150)
    lower_limit = models.FloatField()
    upper_limit = models.FloatField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'Fee_limit'
        unique_together = ('educational_level', 'fee_type')

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
    da_amount = models.FloatField(default=0,null=True)
    hra_amount = models.FloatField(default=0,null=True)
    ta_amount = models.FloatField(default=0,null=True)
    agp_amount = models.FloatField(default=0,null=True)
    basic_pay = models.FloatField()
    salary_date = models.DateField()
    approval_status = models.CharField(max_length=20,null=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    payment_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = 'Salary_transaction'

class Student_fee_transaction(models.Model):
    sft_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_register,on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Academic_year,on_delete=models.SET_NULL,null=True)
    student_fee = models.ForeignKey(Student_fee,on_delete=models.SET_NULL,null=True)
    total_amount = models.FloatField()
    payment_date = models.DateField()
    created_at = models.DateField()
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    late_payment_days = models.IntegerField(default=0)
    late_payment_penalty = models.FloatField(default=0)
    due_date = models.DateField(null=True)

    def calculate_due_date(self):
        if not self.student_fee:
            return None
        
        academic_year = self.academic_year
        if not academic_year:
            return None

        term = self.student_fee.term
        year = academic_year.start_date.year

        if term == '1':  # First Term
            return timezone.datetime(year, 8, 31).date()
        elif term == '2':  # Second Term
            return timezone.datetime(year, 11, 30).date()
        elif term == '3':  # Third Term
            return timezone.datetime(year + 1, 3, 31).date()
        return None

    def calculate_late_payment_penalty(self):
        if not self.due_date or not self.payment_date:
            return 0
        
        if self.payment_date <= self.due_date:
            return 0
            
        days_late = (self.payment_date - self.due_date).days
        self.late_payment_days = days_late
        penalty = days_late * 10  # ₹10 per day
        return penalty

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.calculate_due_date()
        
        if not self.late_payment_penalty:
            self.late_payment_penalty = self.calculate_late_payment_penalty()
            self.total_amount += self.late_payment_penalty
            
        super().save(*args, **kwargs)

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
    staff = models.ForeignKey(Staff_register, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(Leave_type, on_delete=models.SET_NULL, null=True)
    reason = models.TextField() 
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, null=True)
    academic_year = models.ForeignKey(Academic_year, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Staff_leave'

    def clean(self):
        if not self.leave_type:
            return

        # Get the start and end dates of the month
        month_start = self.start_date.replace(day=1)
        if self.start_date.month == 12:
            next_month = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)
        else:
            next_month = self.start_date.replace(month=self.start_date.month + 1, day=1)
        month_end = next_month - timezone.timedelta(days=1)

        # Get all approved leaves for this staff in the current month
        monthly_leaves = Staff_leave.objects.filter(
            staff=self.staff,
            leave_type=self.leave_type,
            start_date__gte=month_start,
            end_date__lte=month_end,
            status='approved'
        ).exclude(sl_id=self.sl_id)

        # Calculate total days of leave taken this month
        total_days_this_month = sum(leave.no_of_days for leave in monthly_leaves)
        total_days_this_month += self.no_of_days

        # Check if exceeds monthly limit
        if total_days_this_month > self.leave_type.max_days_per_month:
            raise ValidationError(
                f'Cannot take more than {self.leave_type.max_days_per_month} {self.leave_type.leave_type} days in a month. '
                f'Already taken: {total_days_this_month - self.no_of_days} days'
            )

        # Get all approved leaves for this staff in the current academic year
        if self.academic_year:
            yearly_leaves = Staff_leave.objects.filter(
                staff=self.staff,
                leave_type=self.leave_type,
                academic_year=self.academic_year,
                status='approved'
            ).exclude(sl_id=self.sl_id)

            total_days_this_year = sum(leave.no_of_days for leave in yearly_leaves)
            total_days_this_year += self.no_of_days

            if total_days_this_year > self.leave_type.days:
                raise ValidationError(
                    f'Cannot take more than {self.leave_type.days} {self.leave_type.leave_type} days in an academic year. '
                    f'Already taken: {total_days_this_year - self.no_of_days} days'
                )

class BlockchainRecord(models.Model):
    index = models.IntegerField()
    timestamp = models.FloatField()
    data = models.JSONField()
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)

    class Meta:
        db_table = 'BlockchainRecord'
        ordering = ['index']

class StudentPromotion(models.Model):
    sp_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_register, on_delete=models.CASCADE)
    from_standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='promotions_from')
    to_standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='promotions_to')
    academic_year = models.ForeignKey(Academic_year, on_delete=models.CASCADE)
    promotion_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'StudentPromotion'

class AttendanceStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name

    class Meta:
        db_table = 'Attendance_status'

class StaffAttendance(models.Model):
    sa_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff_register, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    attendance_status = models.ForeignKey(AttendanceStatus, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(Academic_year, on_delete=models.CASCADE)
    marked_by = models.ForeignKey(Login, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Staff_attendance'
        unique_together = ['staff', 'attendance_date', 'academic_year']