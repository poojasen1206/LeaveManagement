# Generated by Django 3.2.2 on 2021-06-10 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave_management', '0003_my_leave_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave_form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100)),
                ('application_date', models.DateTimeField(blank=True)),
                ('remaining_leave', models.IntegerField(blank=True, null=True)),
                ('from_date', models.DateField(blank=True)),
                ('till_date', models.DateField(blank=True)),
                ('total_taken_leave', models.CharField(blank=True, max_length=100, null=True)),
                ('day', models.CharField(blank=True, max_length=100, null=True)),
                ('remark', models.TextField(blank=True, max_length=2000)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='leave_attachment/')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created', to=settings.AUTH_USER_MODEL)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_t', to='leave_management.leave_type')),
            ],
        ),
    ]
