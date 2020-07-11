from django.urls import path, register_converter
from apps.dashboard import views

urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
]