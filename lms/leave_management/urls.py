
from django.urls import path
from . import views

app_name = 'leave_management'

urlpatterns = [
    # path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leave_form/', views.leave_form, name='leave_form'),
    path('my_leave_record/', views.my_leave_record, name='my_leave_record'),
    path('my_leave_record/<int:pk>/extend_leave', views.extend_leave, name='extend_leave'),
    path('my_leave_record/<int:pk>/extend_approved_leave', views.extend_approved_leave, name='extend_approved_leave'),
    path('leave_structure/', views.leave_structure, name='leave_structure'),


    path('leave_structure/<int:pk>/edit_leave_type/', views.edit_leave_type, name='edit_leave_type'),
    path('leave_structure/<int:pk>/delete_leave_type/', views.delete_leave_type, name='delete_leave_type'),
    path('leave_structure/<int:pk>/edit_holiday/', views.edit_holiday, name='edit_holiday'),
    path('leave_structure/<int:pk>/delete_holiday/', views.delete_holiday, name='delete_holiday'),
    path('leave_structure/<int:pk>/edit_work_week/', views.edit_work_week, name='edit_work_week'),
    path('leave_structure/<int:pk>/delete_work_week/', views.delete_work_week, name='delete_work_week'),

    path('my_leave_balance/', views.my_leave_balance, name='my_leave_balance'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('ajax-posting/', views.ajax_posting, name='ajax_posting'),
    path('ajax_extend_leave/', views.ajax_extend_leave, name='ajax_extend_leave'),
   

]
