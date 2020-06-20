from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from .forms import *
from apps.teachers.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from itertools import chain

# Create your views here.

# tests if user is teacher
def is_teacher(user):
    return user.is_teacher

@login_required
@user_passes_test(is_teacher)
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
@user_passes_test(is_teacher)
def choose_question_type(request, survey_id):
    if request.method == 'POST':
        form = QuestionTypeForm(request.POST)
        if form.is_valid():
            question_type_choice = form.cleaned_data["question_type_choice"]
            if question_type_choice == "boolean":
                return redirect("add_boolean_question", survey_id=survey_id)
            elif question_type_choice == "text":
                return redirect("add_text_question", survey_id=survey_id)
            elif question_type_choice == "mc":
                return redirect("add_mc_question", survey_id=survey_id)
            elif question_type_choice == "checkbox":
                return redirect("add_checkbox_question", survey_id=survey_id)

    else:
        form = QuestionTypeForm()
    return render(request, "teachers/choose_question_type.html", {'form': form,
                                                                  'survey_id': survey_id})

@login_required
@user_passes_test(is_teacher)
def add_boolean_question(request, survey_id):
    if request.method == 'POST':
        form = BooleanQuestionForm(request.POST)
        if form.is_valid():
            survey = Survey.objects.get(pk=survey_id)
            boolean_question = form.save(commit=False)
            boolean_question.survey = survey
            objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                            survey.mc_questions.count() + survey.checkbox_questions.count()
            boolean_question.question_rank = objects_count + 1
            boolean_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)

    else:
        form = BooleanQuestionForm()
    return render(request, "teachers/add_boolean_question.html", {'form': form,
                                                                  'survey_id': survey_id})

@login_required
@user_passes_test(is_teacher)
def add_text_question(request, survey_id):
    if request.method == 'POST':
        form = TextQuestionForm(request.POST)
        if form.is_valid():
            survey = Survey.objects.get(pk=survey_id)
            text_question = form.save(commit=False)  # commit=False means we want to get the object from the form w/o saving it to DB
            text_question.survey = survey
            objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                            survey.mc_questions.count() + survey.checkbox_questions.count()
            text_question.question_rank = objects_count + 1
            text_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)
    else:
        form = TextQuestionForm()
    return render(request, "teachers/add_text_question.html", {'form': form,
                                                               'survey_id': survey_id})

@login_required
@user_passes_test(is_teacher)
def add_mc_question(request, survey_id):
    # for this form we can make the first 2 answer fields required and the next 3 optional
    if request.method == 'POST':
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            survey = Survey.objects.get(pk=survey_id)
            text_question = form.save(commit=False)
            text_question.survey = survey
            objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                            survey.mc_questions.count() + survey.checkbox_questions.count()
            text_question.question_rank = objects_count + 1
            text_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)
    else:
        form = MultipleChoiceQuestionForm()
    return render(request, "teachers/add_mc_question.html", {'form': form,
                                                             'survey_id': survey_id})

@login_required
@user_passes_test(is_teacher)
def add_checkbox_question(request, survey_id):
    # same as above.
    if request.method == 'POST':
        form = CheckboxQuestionForm(request.POST)
        if form.is_valid():
            survey = Survey.objects.get(pk=survey_id)
            text_question = form.save(commit=False)
            text_question.survey = survey
            objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                            survey.mc_questions.count() + survey.checkbox_questions.count()
            text_question.question_rank = objects_count + 1
            text_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey=survey_id)
    else:
        form = CheckboxQuestionForm()
    return render(request, "teachers/add_checkbox_question.html", {'form': form,
                                                                   'survey_id': survey_id})

@login_required
@user_passes_test(is_teacher)
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

    return render(request, "teachers/view_recurring_questions.html", {"questions": recurring_question_list,
                                                                      "base_survey_id": baseSurvey.pk})


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, "teachers/dashboard.html")

@login_required
@user_passes_test(is_teacher)
def view_classes(request):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    return render(request, "teachers/view_classes.html", {'class_list': class_list})

@login_required
@user_passes_test(is_teacher)
def view_questions(request, survey_id):
    boolean_questions = BooleanQuestion.objects.filter(survey=survey_id)
    text_questions = TextQuestion.objects.filter(survey=survey_id)
    mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey_id)
    checkbox_questions = CheckboxQuestion.objects.filter(survey=survey_id)

    question_list = list(chain(boolean_questions, text_questions, mc_questions,
                                         checkbox_questions))
    return render(request, "teachers/view_questions.html", {"questions": question_list,
                                                                      "survey_id": survey_id})

@login_required
@user_passes_test(is_teacher)
def add_survey(request, classroom_id):
    if request.method == 'POST':
        form = SurveyCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["survey_name"]
            new_survey = Survey.objects.create(name=name, classroom_id=classroom_id)
            return redirect("view_questions", survey_id=new_survey.id)

    else:
        form = SurveyCreationForm()

    return render(request, "teachers/add_survey.html", {'form': form})

@login_required
@user_passes_test(is_teacher)
def view_classroom_info(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    surveys = Survey.objects.filter(classroom_id=classroom_id).exclude(name="Base")
    return render(request, "teachers/view_classroom_info.html", {'classroom': classroom, 'surveys': surveys})


@login_required
@user_passes_test(is_teacher)
def suggest_feature(request):
    return render(request, "teachers/suggest_feature.html")

@login_required
@user_passes_test(is_teacher)
def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))