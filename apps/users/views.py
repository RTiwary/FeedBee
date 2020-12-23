from django.shortcuts import render, redirect
from .forms import RegistrationForm
from apps.users.models import Student, Teacher
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


def homepage(request):
    return render(request, "users/landing_page.html")


def terms_conditions(request):
    return render(request, "users/terms-conditions.html")


def privacy_policy(request):
    return render(request, "users/privacy-policy.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if user.is_student:
                Student.objects.create(user=user)
                return redirect(reverse("join_class"))
            else:
                Teacher.objects.create(user=user)
                return redirect(reverse("add_class"))
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('external_login')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if user.is_teacher:
                    return redirect(reverse("dash"))
                else:
                    return redirect('student_dashboard')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="users/login.html",
                  context={"form": form})


def external_login_request(request):
    # Retrieve email address of logged in user and check database
    email = request.user.email
    is_student = True if len(Student.objects.filter(user__email=email)) == 1 else False
    is_teacher = True if len(Teacher.objects.filter(user__email=email)) == 1 else False
    if not is_student and not is_teacher:
        form = AuthenticationForm() # change to timezone form later
        return render(request=request,
                      template_name="users/login.html",
                      context={"form": form})
    elif is_student:
        return redirect('student_dashboard')
    else:
        return redirect('teacher_dashboard')
