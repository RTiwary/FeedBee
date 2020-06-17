from django.urls import path
from apps.students import views

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name="student_dashboard"),
    path('join_class/', views.join_class, name="join_class"),
    path('view_classes/', views.view_classes, name="view_classes"),
    path('suggest_feature/', views.suggest_feature, name="suggest_feature"),
    path('take_survey<int:survey_id>', views.take_survey, name="take_survey"),
    path('logout/', views.logout_request, name="logout"),
]