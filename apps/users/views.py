from django.shortcuts import render, redirect
from .forms import RegistrationForm
from apps.users.models import Student, Teacher


# Create your views here.
def homepage(request):
    return render(request, "users/home.html")

def register_student(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()
            Student.objects.create(user=user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

def register_teacher(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True
            user.save()
            Teacher.objects.create(user=user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

def login(request):
    return render(request, "users/login.html")
