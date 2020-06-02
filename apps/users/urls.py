from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name='login'),
    path('register_student/', views.register_student, name="register_student"),
    path('register_teacher/', views.register_teacher, name="register_teacher"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_password_form.html')),
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/reset_password_form.html')),
]