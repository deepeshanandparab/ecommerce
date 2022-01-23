from django.urls import path
from .views import signup, login, logout, myart, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', signup, name='signuppage'),
    path('login', login, name='loginpage'),
    path('myart', myart, name='myartpage'), 
    path('profile', profile, name='profilepage'),
    path('logout', logout, name='logoutpage'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html'),
         name='password_reset_confirm'),   
]
