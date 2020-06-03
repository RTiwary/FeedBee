from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name='login'),
    path('register_student/', views.register_student, name="register_student"),
    path('register_teacher/', views.register_teacher, name="register_teacher"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html')),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html')),
    path('password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html')),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html')),
]