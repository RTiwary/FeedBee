from django.urls import path, register_converter
from apps.dashboard import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('teacher_dashboard/', views.dash, name="dash"),
    path('teacher_dashboard/<int:classroom_id>/', views.dash_select, name="dash_select"),
    path('teacher_dashboard/<int:classroom_id>/<int:survey_id>', views.teacher_dashboard, name="teacher_dashboard"),
]