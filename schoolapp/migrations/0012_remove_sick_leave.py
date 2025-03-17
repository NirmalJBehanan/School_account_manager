from django.db import migrations

def remove_sick_leave_and_setup_defaults(apps, schema_editor):
    Leave_type = apps.get_model('schoolapp', 'Leave_type')
    Staff_leave = apps.get_model('schoolapp', 'Staff_leave')
    
    # Delete any sick leave applications
    Staff_leave.objects.filter(
        leave_type__leave_type__icontains='sick'
    ).delete()
    
    # Delete any leave types except casual and vacation
    Leave_type.objects.exclude(
        leave_type__in=['casual', 'vacation']
    ).delete()
    
    # Ensure casual leave exists with correct values
    casual_leave, created = Leave_type.objects.get_or_create(
        leave_type='casual',
        defaults={
            'days': 15,
            'max_days_per_month': 5,
            'status': True
        }
    )
    if not created:
        casual_leave.days = 15
        casual_leave.max_days_per_month = 5
        casual_leave.status = True
        casual_leave.save()
    
    # Ensure vacation leave exists with correct values
    vacation_leave, created = Leave_type.objects.get_or_create(
        leave_type='vacation',
        defaults={
            'days': 30,
            'max_days_per_month': 5,
            'status': True
        }
    )
    if not created:
        vacation_leave.days = 30
        vacation_leave.max_days_per_month = 5
        vacation_leave.status = True
        vacation_leave.save()

def reverse_func(apps, schema_editor):
    # This is a one-way migration, no reverse operation needed
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('schoolapp', '0011_leave_type_max_days_per_month_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_sick_leave_and_setup_defaults, reverse_func),
    ] 