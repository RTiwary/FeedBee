from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from .forms import ClassroomCreationForm
from apps.teachers.models import *
from django.contrib.auth.decorators import login_required, permission_required
from itertools import chain

# Create your views here.
@login_required
@permission_required("user.is_teacher", raise_exception=True)
def add_class(request):
    if request.method == 'POST':
        form = ClassroomCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["class_name"]
            teacher = request.user.teacher_profile
            created_classroom = Classroom.objects.create(name=name, teacher=teacher)
            return redirect("view_recurring_questions", classroom_id=created_classroom.pk)

    else:
        form = ClassroomCreationForm()

    return render(request, "teachers/add_class.html", {'form': form})


@login_required
@permission_required("user.is_teacher", raise_exception=True)
def add_recurring_question(request):
    return render(request, "teachers/add_recurring_question.html")

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def view_recurring_questions(request, classroom_id):
    base_survey_queryset = Survey.objects.filter(name="Base").filter(classroom_id=classroom_id)
    if not base_survey_queryset:
        survey_classroom = Classroom.objects.get(id=classroom_id)
        baseSurvey = Survey.objects.create(name="Base", classroom=survey_classroom)
    else:
        baseSurvey = base_survey_queryset[0]

    recurring_boolean_questions = BooleanQuestion.objects.filter(survey=baseSurvey)
    recurring_text_questions = TextQuestion.objects.filter(survey=baseSurvey)
    recurring_mc_questions = MultipleChoiceQuestion.objects.filter(survey=baseSurvey)
    recurring_checkbox_questions = CheckboxQuestion.objects.filter(survey=baseSurvey)

    recurring_question_list = list(chain(recurring_boolean_questions, recurring_text_questions, recurring_mc_questions,
                                         recurring_checkbox_questions))

    return render(request, "teachers/view_recurring_questions.html", {"questions": recurring_question_list})

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def teacher_dashboard(request):
    return render(request, "teachers/dashboard.html")

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def view_classes(request):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    return render(request, "teachers/view_classes.html", {'class_list': class_list})

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def view_surveys(request, classroom_id):
    survey_list = Survey.objects.filter(classroom_id=classroom_id)
    return render(request, "teachers/view_surveys.html", {'survey_list': survey_list})

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def suggest_feature(request):
    return render(request, "teachers/suggest_feature.html")

@login_required
@permission_required("user.is_teacher", raise_exception=True)
def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))