from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.http.response import HttpResponseRedirect,HttpResponse
from datetime import date,  timedelta
from django.db.models import Q
from django.http import JsonResponse
import pandas as pd








# Create your views here.

def index(request):
    return render(request, 'leave_management/index.html')

@login_required
def dashboard(request):
    return render(request, 'leave_management/dashboard.html')



 

def leave_form(request):
    leave_type = Leave_type.objects.filter(typeleave='Leave type').distinct()

    leave = My_leave_balance.objects.filter(created_by = request.user.id).values_list('leave_name','leave_remaining')
    if not leave:
        leave = Leave_type.objects.all().values_list('id', 'leave_per_year')
    leave_dict = dict(leave)

    holiday_list = []
    holiday = Leave_type.objects.filter(typeleave='Holiday')
    for i in holiday:
        date_str = str(i.date)
        holiday_list.append(date_str)





    if request.method == 'POST':
        leave_formobj = Leave_form()
        leave_formobj.employee_name     = request.POST.get('employee_name')
        leave_formobj.application_date  = request.POST.get('current_date')
        leave_formobj.leave_type_id     = request.POST.get('leave_type')
        leave_formobj.remaining_leave   = request.POST.get('remaining_leave')
        date_from                       = request.POST.get('from_date')
        leave_formobj.from_date         = datetime.strptime(date_from, "%m/%d/%Y").strftime("%Y-%m-%d")
        date_till                       = request.POST.get('till_date')
        leave_formobj.till_date         = datetime.strptime(date_till, "%m/%d/%Y").strftime("%Y-%m-%d")
        leave_formobj.day               = request.POST.get('day')
        leave_formobj.total_taken_leave = request.POST.get('total_taken_leave')
        leave_formobj.remark            = request.POST.get('remark')
        leave_formobj.attachment        = request.FILES.get('myfile')
        leave_formobj.status            = request.POST.get('status')
        leave_formobj.created_by_id     = request.user.id
        leave_formobj.save()
        return redirect('leave_management:my_leave_record')
    else:
        return render(request,'leave_management/leave_form.html',{'leave_type':leave_type,'leave_dict':leave_dict,'holiday_list':holiday_list})


def my_leave_record(request):
    # date =datetime.now().strftime('%F %d,%Y,')
    # time = datetime.now().strftime('%H')
    # time1 = datetime.strptime('10','%H')
    # t1 = time1.strftime('%H')

    leave_type = Leave_type.objects.filter(typeleave='Leave type').distinct()

    if request.method == 'POST':
        data = request.POST
        if data.get('leave_name'):
            leave_type = Leave_type.objects.filter(leave_type=data.get('leave_type'))


        if data.get('from_date'):
            if data.get('to_date'):
                start_date = data.get('from_date')
                end_date = data.get('to_date')
                leave_form = Leave_form.objects.filter(
                    Q(from_date__gte=start_date) & Q(till_date__lte=end_date)
                )
            else:
                start_date = data.get('from_date')
                end_date = data.get('to_date')
                leave_form = Leave_form.objects.filter(
                    Q(from_date__gte=start_date) & Q(till_date__lte=end_date)
                )

            return render(request,'leave_management/my_leave_record.html', {'leave_form':leave_form,'leave_type':leave_type})

    leave_form = Leave_form.objects.all().order_by('-application_date')
    final_status = Leave_form.objects.filter(id=request.POST.get('withdraw')).first()

    if request.method == 'POST':
        get_leave_type = Leave_type.objects.filter(id=final_status.leave_type.id).first()
        remaining_leave = int(final_status.remaining_leave) + int(final_status.total_taken_leave)
        my_leave_balanceobj = My_leave_balance.objects.filter(leave_name=get_leave_type.id).first()

        final_status.status = 'Withdraw'
        final_status.remaining_leave = remaining_leave
        final_status.save()

        if my_leave_balanceobj:
            my_leave_balanceobj.leave_name_id = get_leave_type.id
            my_leave_balanceobj.leave_remaining = remaining_leave
            my_leave_balanceobj.created_by_id = request.user.id
            my_leave_balanceobj.save()

        return redirect('leave_management:my_leave_record')

    return render(request,'leave_management/my_leave_record.html', {'leave_form':leave_form,'date':date,'leave_type':leave_type})


def extend_leave(request,pk):
    extend_leave = Leave_form.objects.filter(id=pk).first()
    data = {'extend_leave': extend_leave}

    if request.method == 'POST':
        if request.POST['employee_name']:
            extend_leave.employee_name = request.POST["employee_name"]
        if request.POST['current_date']:
            extend_leave.application_date = request.POST['current_date']
        if request.POST['leave_type']:
            extend_leave.leave_type_id = request.POST['leave_type']
        if request.POST['remaining_leave']:
            extend_leave.remaining_leave = request.POST['remaining_leave']
        if request.POST['from_date']:
            date_from = request.POST['from_date']
            extend_leave.from_date=datetime.strptime(date_from, "%m/%d/%Y").strftime("%Y-%m-%d")
        if request.POST['till_date']:
            date_till = request.POST['till_date']
            extend_leave.till_date = datetime.strptime(date_till, "%m/%d/%Y").strftime("%Y-%m-%d")
        if request.POST['total_taken_leave']:
            extend_leave.total_taken_leave = request.POST['total_taken_leave']
        if request.POST['remark']:
            extend_leave.remark = request.POST['remark']
        extend_leave.save()
        return redirect('leave_management:my_leave_record')

    return render(request, 'leave_management/extend_leave.html',data)

def extend_approved_leave(request,pk):
    extend_approved_leave = Leave_form.objects.filter(id=pk).first()
    data = {'extend_approved_leave': extend_approved_leave}

    if request.method == 'POST':
        leave_formobj = Leave_form()
        if request.POST['employee_name']:
            leave_formobj.employee_name = request.POST["employee_name"]
        if request.POST['current_date']:
            leave_formobj.application_date = request.POST['current_date']
        if request.POST['leave_type']:
            leave_formobj.leave_type_id = request.POST['leave_type']
        if request.POST['remaining_leave']:
            leave_formobj.remaining_leave = request.POST['remaining_leave']
        if request.POST['from_date']:
            date_from = request.POST['from_date']
            leave_formobj.from_date=datetime.strptime(date_from, "%m/%d/%Y").strftime("%Y-%m-%d")
        if request.POST['till_date']:
            date_till = request.POST['till_date']
            leave_formobj.till_date = datetime.strptime(date_till, "%m/%d/%Y").strftime("%Y-%m-%d")
        if request.POST['total_taken_leave']:
            leave_formobj.total_taken_leave = request.POST['total_taken_leave']
        if request.POST['remark']:
            leave_formobj.remark = request.POST['remark']
        leave_formobj.attachment = request.FILES.get('myfile')
        leave_formobj.day        = request.POST.get('day')
        leave_formobj.status     = request.POST.get('status')
        leave_formobj.created_by_id = request.user.id
        leave_formobj.save()
        return redirect('leave_management:my_leave_record')

    return render(request,'leave_management/extend_approved_leave.html',data)


def leave_structure(request):

    leave_type   = Leave_type.objects.filter(typeleave = 'Leave type')
    holiday      = Leave_type.objects.filter(typeleave = 'Holiday')
    work_week    = Work_week_plan.objects.all()
    leave_policy = Leave_policy.objects.all()
    
    if request.method == 'POST':
        leave_typeobj = Leave_type()
        if request.POST.get('leave_name'):
            leave_typeobj.typeleave = 'Leave Type'
            leave_typeobj.leave_name = request.POST.get('leave_name')
            leave_typeobj.leave_rule = request.POST.get('leave_rule')
            leave_typeobj.leave_per_year = request.POST.get('leave_per_year')
            leave_typeobj.leave_carried_forward = request.POST.get('leave_carried_forward')
            leave_typeobj.remaining_leave = request.POST.get('leave_per_year')
            leave_typeobj.created_by_id     = request.user.id
            leave_typeobj.save()

        elif request.POST.get('holiday_name'):
            leave_typeobj.typeleave = 'Holiday'
            leave_typeobj.holiday_name = request.POST.get('holiday_name')
            if request.POST['date']:
                leave_typeobj.date = request.POST.get('date')
            if request.POST['holiday_country']:
                leave_typeobj.country = request.POST.get('holiday_country')
            leave_typeobj.created_by_id     = request.user.id
            leave_typeobj.save()

        elif request.POST.get('leave_policy'):
            leave_policyobj = Leave_policy()
            leave_policyobj.leave_policy = request.POST.get('leave_policy')
            leave_policyobj.created_by_id = request.user.id
            leave_policyobj.save()

        else:
            week_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            checkbox_list = request.POST.getlist('checks[]')

            for i in week_list:
                if i in checkbox_list:
                        work_week_planobj = Work_week_plan()
                        work_week_planobj.week_day = i
                        work_week_planobj.working_off = 'Working'
                        work_week_planobj.country = request.POST.get('work_week_country')
                        work_week_planobj.created_by_id     = request.user.id
                        work_week_planobj.save()
                else:
                    work_week_planobj = Work_week_plan()
                    work_week_planobj.week_day = i
                    work_week_planobj.working_off = 'Off'
                    work_week_planobj.country = request.POST.get('work_week_country')
                    work_week_planobj.created_by_id     = request.user.id
                    work_week_planobj.save()

        return redirect('leave_management:leave_structure')
    else:
        return render(request, 'leave_management/leave_structure.html', {'leave_type':leave_type, 'holiday':holiday, 'work_week':work_week,'leave_policy':leave_policy})

def edit_leave_type(request,pk):

    leave_type = Leave_type.objects.filter(id=pk).first()
    data = {'leave_type':leave_type}

    if request.method == 'POST':
        if request.POST['leave_name']:
            leave_type.leave_name = request.POST["leave_name"]
        if request.POST['leave_rule']:
            leave_type.leave_rule = request.POST['leave_rule']
        if request.POST['leave_per_year']:
            leave_type.leave_per_year = request.POST['leave_per_year']
        if request.POST['leave_carried_forward']:
            leave_type.leave_carried_forward = request.POST['leave_carried_forward']

        leave_type.save()
        return redirect('leave_management:leave_structure')

    return render(request,'leave_management/edit_leave_type.html', data)

def delete_leave_type(request,pk):
    leave_type = Leave_type.objects.filter(id=pk).delete()
    return redirect('leave_management:leave_structure')


def edit_holiday(request, pk):
    holiday = Leave_type.objects.filter(id=pk).first()
    data = {'holiday':holiday}
    if request.method == 'POST':
        if request.POST['holiday_name']:
            holiday.holiday_name = request.POST['holiday_name']
        if request.POST['date']:
            holiday.date = request.POST['date']
        if request.POST['holiday_country']:
            holiday.holiday_country = request.POST['holiday_country']
        holiday.save()
        return redirect('leave_management:leave_structure')

    return render(request,'leave_management/edit_holiday.html', data)


def delete_holiday(request,pk):
    leave_type = Leave_type.objects.filter(id=pk).delete()
    return redirect('leave_management:leave_structure')

def edit_work_week(request,pk):
    if request.method == 'POST':
        work_week = Work_week_plan.objects.filter(id = pk).first()

        if request.POST.get('working') != None:
            work_week.working_off = request.POST.get('working')
            work_week.save()

        else:
            work_week.working_off = 'Off'
            work_week.save()

        return redirect('leave_management:leave_structure')


def delete_work_week(request,pk):
    work_week = Work_week_plan.objects.filter(id=pk).delete()
    return redirect('leave_management:leave_structure')



def my_leave_balance(request):
    leave_type = Leave_type.objects.filter(typeleave='Leave type')
    leave_balance = My_leave_balance.objects.filter(created_by = request.user.id)

    return render(request, 'leave_management/my_leave_balance.html', {'leave_type':leave_type, 'leave_balance':leave_balance})




def leave_request(request):

    leave_form = Leave_form.objects.all().order_by('-application_date')
    final_status = Leave_form.objects.filter(id = request.POST.get('approval')).first()

    if request.method == 'POST':
        get_leave_type = Leave_type.objects.filter(id=final_status.leave_type.id).first()
        remaining_leave = int(final_status.remaining_leave) - int(final_status.total_taken_leave)
        my_leave_balanceobj = My_leave_balance.objects.filter(leave_name = get_leave_type.id, created_by = request.user.id).first()
        if final_status.status == 'Approved':
            print('hello')
        else:
            if request.POST.get('status')=='Approve':
                final_status.status = 'Approved'
                final_status.remaining_leave = remaining_leave
                final_status.save()
                if my_leave_balanceobj:
                    my_leave_balanceobj.leave_name_id = get_leave_type.id
                    my_leave_balanceobj.leave_remaining = remaining_leave
                    my_leave_balanceobj.created_by_id = request.user.id
                    my_leave_balanceobj.save()

                else:
                    my_leave_balanceobj = My_leave_balance()
                    my_leave_balanceobj.leave_name_id = get_leave_type.id
                    my_leave_balanceobj.leave_remaining = remaining_leave
                    my_leave_balanceobj.created_by_id = request.user.id
                    my_leave_balanceobj.save()

            elif request.POST.get('status')=='Reject':
                if final_status.status == 'Approved':
                    remaining_leave = int(final_status.remaining_leave) + int(final_status.total_taken_leave)
                    my_leave_balanceobj = My_leave_balance.objects.filter(leave_name=get_leave_type.id).first()
                    final_status.status = 'Rejected'
                    final_status.remaining_leave = remaining_leave
                    final_status.reject_reason = request.POST.get('reason_for_rejection')
                    final_status.save()
                    if my_leave_balanceobj:
                        my_leave_balanceobj.leave_name_id = get_leave_type.id
                        my_leave_balanceobj.leave_remaining = remaining_leave
                        my_leave_balanceobj.created_by_id = request.user.id
                        my_leave_balanceobj.save()
                else:
                    final_status.status = 'Rejected'
                    final_status.reject_reason = request.POST.get('reason_for_rejection')
                    final_status.save()
            return redirect('leave_management:leave_request')
    return render(request, 'leave_management/leave_request.html',{'leave_form':leave_form})

def ajax_posting(request):
    date1 = request.POST.get('date1', None)
    date2 = request.POST.get('date2', None)

    sdate = datetime. strptime(date1,'%Y-%m-%d')
    edate = datetime. strptime(date2,'%Y-%m-%d')

    delta = edate - sdate

    dates = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))

    # date = pd.DataFrame({'inputDate': dates})
    # date['inputDate'] = pd.to_datetime(date['inputDate'])
    # date['dayOfWeek'] = date['inputDate'].dt.day_name()
    # daylist = date['dayOfWeek'].tolist()
    # find_day = daylist.index('Sunday')

    holiday_list = []
    holiday = Leave_type.objects.filter(typeleave='Holiday')
    for i in holiday:
        date_str =str(i.date)
        holiday_list.append(date_str)

    count = 0
    for i in dates:
        if not i in holiday_list:
            count = count+1

    response = {
        'count': count
    }
    return JsonResponse(response)


def ajax_extend_leave(request):
    date1 = request.POST.get('date1', None)
    date2 = request.POST.get('date2', None)

    sdate = datetime.strptime(date1, '%Y-%m-%d')
    edate = datetime.strptime(date2, '%Y-%m-%d')

    delta = edate - sdate

    dates = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))


    leave_date = []
    leave = Leave_form.objects.filter()
    print(leave)
    for i in leave:
        date_str = str(i.from_date)
        leave_date.append(date_str)



    count = 0

    response = {
        'count': count
    }
    return JsonResponse(response)

