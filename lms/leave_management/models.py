from django.db import models
from django.contrib.auth.models import User
from common.models import User






# Create your models here.


class Leave_type(models.Model):
    leave_name = models.CharField(max_length=100)
    leave_rule = models.CharField(max_length=100, null=True, blank=True)
    leave_per_year = models.CharField(max_length=100, null=True, blank=True)
    leave_carried_forward = models.CharField(max_length=100, null=True, blank=True)
    holiday_name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    typeleave = models.CharField(max_length=50, default='', blank=True)
    created_by = models.ForeignKey(User, related_name='create_by', on_delete=models.CASCADE, null=True)


class Work_week_plan(models.Model):
    week_day = models.CharField(max_length=100, null=True, blank=True)
    working_off = models.CharField(max_length=50, default=0, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='create', on_delete=models.CASCADE, null=True)




class My_leave_balance(models.Model):
    leave_name = models.ForeignKey(Leave_type, related_name="leavename", on_delete=models.CASCADE)
    leave_remaining = models.IntegerField(blank=True , default=0)
    created_by = models.ForeignKey(User, related_name='createdby', on_delete=models.CASCADE, null=True)



class Leave_form(models.Model):
    employee_name = models.CharField(max_length=100)
    application_date = models.DateField(auto_now_add=False, blank=True)
    leave_type = models.ForeignKey(Leave_type, related_name="leave_t", on_delete=models.CASCADE)
    remaining_leave = models.IntegerField(blank=True, null=True)
    from_date = models.DateField(auto_now_add=False, blank=True)
    till_date = models.DateField(auto_now_add=False, blank=True)
    total_taken_leave = models.CharField(max_length=100, null=True, blank=True)
    day = models.CharField(max_length=100, null=True, blank=True)
    remark = models.TextField(max_length=2000,blank=True)
    attachment = models.FileField(upload_to='leave_attachment/', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='created', on_delete=models.CASCADE, null=True)
    reject_reason = models.CharField(max_length=100, null=True, blank=True)

class Leave_policy(models.Model):
    leave_policy = models.CharField(max_length=2000, blank=True)
    created_by = models.ForeignKey(User, related_name='created_by_leave_policy', on_delete=models.CASCADE, null=True)



