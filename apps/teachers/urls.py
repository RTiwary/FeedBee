from django.urls import path
from apps.teachers import views

urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('add_class/', views.add_class, name="add_class"),
    path('add_boolean_question/<int:survey_id>/', views.add_boolean_question, name="add_boolean_question"),
    path('add_text_question/<int:survey_id>/', views.add_text_question, name="add_text_question"),
    path('add_mc_question/<int:survey_id>/', views.add_mc_question, name="add_mc_question"),
    path('add_checkbox_question/<int:survey_id>/', views.add_checkbox_question, name="add_checkbox_question"),
    path('choose_question_type/<int:survey_id>', views.choose_question_type, name="choose_question_type"),
    path('<int:classroom_id>/view_recurring_questions/', views.view_recurring_questions, name="view_recurring_questions"),
    path('view_classes/', views.view_classes, name="view_classes"),
    path('suggest_feature/', views.suggest_feature, name="suggest_feature"),
    path('logout/', views.logout_request, name="logout"),
]