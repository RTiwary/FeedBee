from django.urls import path, register_converter
from apps.dashboard import views

urlpatterns = [
    path('teacher_dashboard/<int:classroom_id>/<int:survey_id>', views.teacher_dashboard, name="teacher_dashboard"),
]