
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView



urlpatterns = [

    path('', views.indexView,name="home"),
    # path('common/dashboard2/', views.dashboardView,name="dashboard"),
    path('leave_management/dashboard/', views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/', views.registerView,name="register_url"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout")





    
    # path('logout/',LogoutView.as_view(next_page='settings.LOGOUT_REDIRECT_URL'),name="logout"),

    # path('forgot-password/', views.forgot_password, name='forgot-password'),
]
