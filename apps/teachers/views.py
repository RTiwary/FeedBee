from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from apps.teachers.models import *

# Create your views here.
def add_class(request):
    return render(request, "teachers/add_class.html")

def teacher_dashboard(request):
    return render(request, "teachers/dashboard.html")

def view_classes(request):
    return render(request, "teachers/view_classes.html")

def suggest_feature(request):
    return render(request, "teachers/suggest_feature.html")

def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))