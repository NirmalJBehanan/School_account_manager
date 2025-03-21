# Generated by Django 4.2.2 on 2025-03-13 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0008_feelimit'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceStatus',
            fields=[
                ('as_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'Attendance_status',
            },
        ),
        migrations.CreateModel(
            name='StaffAttendance',
            fields=[
                ('sa_id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.academic_year')),
                ('attendance_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.attendancestatus')),
                ('marked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schoolapp.login')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.staff_register')),
            ],
            options={
                'db_table': 'Staff_attendance',
                'unique_together': {('staff', 'attendance_date')},
            },
        ),
    ]
