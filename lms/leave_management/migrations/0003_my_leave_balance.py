# Generated by Django 3.2.2 on 2021-06-10 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave_management', '0002_work_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_leave_balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_remaining', models.IntegerField(blank=True, default=0)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='createdby', to=settings.AUTH_USER_MODEL)),
                ('leave_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leavename', to='leave_management.leave_type')),
            ],
        ),
    ]