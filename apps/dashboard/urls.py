from django.urls import path, register_converter
from apps.dashboard import views
from django.views.decorators.cache import cache_page

app_name = 'dashboard'

urlpatterns = [
    path('teacher_dashboard/', views.dash, name="dash"),
    path('teacher_dashboard/<int:classroom_id>/', views.dash_select, name="dash_select"),
    path('teacher_dashboard/<int:classroom_id>/<int:survey_id>', views.teacher_dashboard, name="teacher_dashboard"),
    path('choose_interval/<int:classroom_id>/<int:survey_id>/', views.choose_interval, name="choose_interval"),
    path('view_individual_responses/<int:classroom_id>/<int:survey_id>/<str:interval>/', views.view_individual_responses, name="view_individual_responses")
]