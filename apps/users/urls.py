from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name='login'),
    path('register_student/', views.register_student, name="register_student"),
    path('register_teacher/', views.register_teacher, name="register_teacher"),
]