from django.shortcuts import render, redirect
from .forms import RegistrationForm
from apps.users.models import Student, Teacher
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
            login(request, user)
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
            login(request, user)
            return redirect(reverse("teacher_dashboard"))
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_teacher:
                    return redirect(reverse("teacher_dashboard"))
                else:
                    return redirect('/') #TODO: change this to student dashboard & add logout view there

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="users/login.html",
                  context={"form": form})
