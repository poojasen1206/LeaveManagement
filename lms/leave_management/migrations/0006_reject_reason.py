# Generated by Django 3.2.2 on 2021-06-17 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management', '0005_application_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_form',
            name='reject_reason',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
