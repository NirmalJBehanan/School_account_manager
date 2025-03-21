# Generated by Django 4.2.2 on 2025-03-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0015_rename_marked_at_staffattendance_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary_transaction',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salary_transaction',
            name='payment_method',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='salary_transaction',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salary_transaction',
            name='payment_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
