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

#dashbaord urls
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
]
