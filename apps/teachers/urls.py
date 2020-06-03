from django.urls import path
from apps.teachers import views

urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('add_class/', views.add_class, name="add_class"),
    path('add_recurring_questions/', views.add_recurring_questions, name="add_recurring_questions"),
    path('view_classes/', views.view_classes, name="view_classes"),
    path('suggest_feature/', views.suggest_feature, name="suggest_feature"),
    path('logout/', views.logout_request, name="logout"),
]