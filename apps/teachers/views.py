from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from .forms import ClassroomCreationForm
from apps.teachers.models import *

# Create your views here.
def add_class(request):
    if request.method == 'POST':
        form = ClassroomCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["class_name"]
            teacher = request.user.teacher_profile
            Classroom.objects.create(name=name, teacher=teacher)
            return redirect(reverse("add_recurring_questions"))

    else:
        form = ClassroomCreationForm()

    return render(request, "teachers/add_class.html", {'form': form})

def add_recurring_questions(request):
    return render(request, "teachers/add_recurring_questions.html")

def teacher_dashboard(request):
    return render(request, "teachers/dashboard.html")

def view_classes(request):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    return render(request, "teachers/view_classes.html", {'class_list': class_list})

def view_surveys(request, classroom_id):
    survey_list = Survey.objects.filter(classroom_id=classroom_id)
    return render(request, "teachers/view_surveys.html", {'survey_list': survey_list})


def suggest_feature(request):
    return render(request, "teachers/suggest_feature.html")

def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))