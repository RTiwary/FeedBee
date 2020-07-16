from django.urls import path, register_converter
from apps.teachers import views

urlpatterns = [
    path('add_class/', views.add_class, name="add_class"),
    path('<int:classroom_id>/delete_class/', views.delete_class, name="delete_class"),
    path('add_boolean_question/<int:survey_id>/', views.add_boolean_question, name="add_boolean_question"),
    path('add_boolean_question/<int:survey_id>/<int:question_id>/', views.add_boolean_question, name="add_boolean_question"),
    path('add_text_question/<int:survey_id>/', views.add_text_question, name="add_text_question"),
    path('add_text_question/<int:survey_id>/<int:question_id>/', views.add_text_question, name="add_text_question"),
    path('add_mc_question/<int:survey_id>/', views.add_mc_question, name="add_mc_question"),
    path('add_mc_question/<int:survey_id>/<int:question_id>/', views.add_mc_question, name="add_mc_question"),
    path('add_checkbox_question/<int:survey_id>/', views.add_checkbox_question, name="add_checkbox_question"),
    path('add_checkbox_question/<int:survey_id>/<int:question_id>/', views.add_checkbox_question, name="add_checkbox_question"),
    path('choose_question_type/<int:survey_id>', views.choose_question_type, name="choose_question_type"),
    path('delete_question/<int:survey_id>/<int:question_id>/<type_id>', views.delete_question, name="delete_question"),
    path('<int:classroom_id>/view_recurring_questions/', views.view_recurring_questions, name="view_recurring_questions"),
    path('view_classroom_info/<int:classroom_id>', views.view_classroom_info, name="view_classroom_info"),
    path('view_classes/', views.view_classes, name="view_classes"),
    path('<int:classroom_id>/add_survey/', views.add_survey, name="add_survey"),
    path('<int:survey_id>/delete_survey/', views.delete_survey, name="delete_survey"),
    path('<int:survey_id>/view_questions/', views.view_questions, name="view_questions"),
    path('<int:survey_id>/view_results/', views.view_results, name="view_results"),
    path('<int:survey_id>/view_results_alt/', views.view_results_alt, name="view_results_alt"),
    path('suggest_feature/', views.suggest_feature, name="suggest_feature"),
    path('logout/', views.logout_request, name="logout"),
]