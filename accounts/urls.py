from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.register, name='register'),
    #this is for register email send which we have written in accountvarification.html url 
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('login/', views.login, name='login'),


    path('logout/', views.logout, name='logout'),


    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    #this is for reset password email send which we have written in resetpassword_email.html url 
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    
    path('resetPassword/', views.resetPassword, name='resetPassword'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
]
