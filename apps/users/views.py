from django.shortcuts import render, redirect
from .forms import RegistrationForm, SocialAdditionalForm
from apps.users.models import Student, Teacher, User
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
                return redirect("teachers:add_class")
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
                    return redirect("dashboard:dash")
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
    # Retrieve user object of logged in user
    user = User.objects.get(email=request.user.email)

    # check if user is a student or teacher and redirects them to correct dashboard
    if user.is_student:
        return redirect('student_dashboard')
    else:
        return redirect('dashboard:dash')


def finish_registration(request):
    user = User.objects.filter(email=request.user.email)
    if request.method == "POST":
        form = SocialAdditionalForm(request.POST)
        if form.is_valid():
            timezone = form.cleaned_data["timezone_choice"]
            if form.cleaned_data["student_teacher"] == "Student":
                user.update(timezone=timezone, is_student=True)
                curr_user = User.objects.get(email=request.user.email)
                # create student profile
                Student.objects.create(user=curr_user)

                return redirect(reverse("join_class"))
            else:
                user.update(timezone=timezone, is_teacher=True)
                curr_user = User.objects.get(email=request.user.email)

                # create teacher profile
                Teacher.objects.create(user=curr_user)

                return redirect("teachers:add_class")
    else:
        form = SocialAdditionalForm()
    return render(request, 'users/social_auth_signup.html', {
        'form': form,
    })


def redirect_login(request):
    messages.error(request, "You created an account through ClassBop but tried to log in with Google/Microsoft. \
                            Please log in through ClassBop instead.")
    return redirect('login')


