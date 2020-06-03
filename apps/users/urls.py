from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

#app_name = 'users'
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name='login'),
    path('register_student/', views.register_student, name="register_student"),
    path('register_teacher/', views.register_teacher, name="register_teacher"),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    #path('', include('django.contrib.auth.urls')),
]