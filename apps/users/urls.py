from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register_student/', views.register_student, name="register_student"),
    path('register_teacher/', views.register_teacher, name="register_teacher"),
]