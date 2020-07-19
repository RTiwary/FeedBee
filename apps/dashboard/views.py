from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.teachers.views import *

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, "dashboard/teacher_dashboard.html")
