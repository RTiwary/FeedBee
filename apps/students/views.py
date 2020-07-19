import calendar
import datetime
import operator

from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from itertools import chain

from django.urls import reverse
from apps.users.models import *
from apps.students.forms import JoinClassForm
from apps.students.models import CheckboxAnswer, TextAnswer, BooleanAnswer, MultipleChoiceAnswer
from apps.teachers.models import CheckboxQuestion, TextQuestion, BooleanQuestion, MultipleChoiceQuestion, Survey, \
    Classroom
from django.contrib.auth.decorators import login_required, user_passes_test


# test for if user is student
def is_student(user):
    return user.is_student


@login_required
@user_passes_test(is_student)
def join_class(request, classroom_id=None):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["class_code"]
            student = request.user.student_profile
            classroom = Classroom.objects.get(pk=code)
            classroom.students.add(student)
            return redirect("student_dashboard")
    elif classroom_id is not None and int(classroom_id) >= 0:
        form = JoinClassForm(initial={"class_code": classroom_id})
        try:
            classroom_name = Classroom.objects.get(pk=int(classroom_id)).name
        except Exception:
            classroom_name = " "
        return render(request, "students/join_class.html", {'form': form, 'classroom_name': classroom_name})

    form = JoinClassForm()
    return render(request, "students/join_class.html", {'form': form})


@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    all_surveys = Survey.objects.filter(classroom__students__user=request.user) \
        .exclude(name="Base").exclude(end_date__lte=datetime.datetime.today())

    surveys, filler = get_pending_surveys(request.user, all_surveys)
    days_due = get_due_days(surveys)

    return render(request, "students/dashboard.html", {
        'surveys': zip(surveys, days_due),
        'empty': len(surveys) == 0
    })


@login_required
@user_passes_test(is_student)
def view_classes(request):
    classes = Classroom.objects.filter(students__user=request.user)

    # getting teacher for each class and converting teacher id to user id
    teacher_list = Classroom.objects.filter(students__user=request.user).values_list('teacher')
    teacher_ids = []
    for teacher in teacher_list:
        teach = Teacher.objects.filter(pk=teacher[0]).values_list('user_id')
        teacher_ids.append(teach)

    # getting each teacher's name
    teachers = []
    for ids in teacher_ids:
        teacher_name = User.objects.filter(pk=ids[0][0]).values('first_name', 'last_name')
        teachers.append(teacher_name.get())

    class_list = zip(classes, teachers)
    return render(request, "students/view_classes.html", {'class_list': class_list})


@login_required
@user_passes_test(is_student)
def view_surveys(request, classroom_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    all_surveys = Survey.objects.filter(classroom=classroom) \
        .exclude(name="Base").exclude(end_date__lte=datetime.datetime.today())

    surveys, completed = get_pending_surveys(request.user, all_surveys)
    days_due = get_due_days(surveys)

    return render(request, "students/view_surveys.html", {'classroom': classroom,
                                                          'surveys': zip(surveys, days_due),
                                                          'completed': completed})


@login_required
@user_passes_test(is_student)
def suggest_feature(request):
    return render(request, "students/suggest_feature.html")


@login_required
@user_passes_test(is_student)
def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))


@login_required
@user_passes_test(is_student)
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    student = request.user.student_profile

    base_survey = Survey.objects.filter(name="Base", classroom=survey.classroom)
    base_questions = []
    if len(base_survey) > 0:
        base_survey = base_survey[0]
        base_bool_questions = BooleanQuestion.objects.filter(survey=base_survey, display=True)
        base_mc_questions = MultipleChoiceQuestion.objects.filter(survey=base_survey, display=True)
        base_txt_questions = TextQuestion.objects.filter(survey=base_survey, display=True)
        base_cb_questions = CheckboxQuestion.objects.filter(survey=base_survey, display=True)
        base_questions = \
            list(chain(base_bool_questions, base_mc_questions, base_txt_questions, base_cb_questions))
        base_questions = sorted(base_questions, key=operator.attrgetter('question_rank'))

    unit_bool_questions = BooleanQuestion.objects.filter(survey=survey)
    unit_mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey)
    unit_txt_questions = TextQuestion.objects.filter(survey=survey)
    unit_cb_questions = CheckboxQuestion.objects.filter(survey=survey)
    unit_questions = \
        list(chain(unit_bool_questions, unit_mc_questions, unit_txt_questions, unit_cb_questions))
    unit_questions = sorted(unit_questions, key=operator.attrgetter('question_rank'))

    questions = list(chain(base_questions, unit_questions))

    if request.method == 'POST':
        if request.POST.get("submit"):
            for q in questions:
                if q.question_type == "Boolean":
                    answer = BooleanAnswer()
                    answer.question = q
                    answer.student = student
                    if request.POST.get(str(q.id) + "_Bool") == "true":
                        answer.answer = True
                    else:
                        answer.answer = False
                    answer.save()

                elif q.question_type == "Text":
                    answer = TextAnswer()
                    answer.question = q
                    answer.student = student
                    if request.POST.get(str(q.id)):
                        answer.answer = request.POST.get(str(q.id))
                        answer.save()

                elif q.question_type == "MultipleChoice":
                    answer = MultipleChoiceAnswer()
                    answer.question = q
                    answer.student = student
                    answer.answer = request.POST.get(str(q.id) + "_MC")
                    answer.save()

                elif q.question_type == "Checkbox":
                    answer = CheckboxAnswer()
                    answer.question = q
                    answer.student = student
                    answer.answer = ""
                    if request.POST.get(str(q.id) + "_A_CB"):
                        answer.answer = "A"
                    if request.POST.get(str(q.id) + "_B_CB"):
                        answer.answer = answer.answer + "B"
                    if request.POST.get(str(q.id) + "_C_CB"):
                        answer.answer = answer.answer + "C"
                    if request.POST.get(str(q.id) + "_D_CB"):
                        answer.answer = answer.answer + "D"
                    if request.POST.get(str(q.id) + "_E_CB"):
                        answer.answer = answer.answer + "E"
                    answer.save()

            return redirect("student_dashboard")

    return render(request, 'students/take_survey.html', {
        'survey': survey,
        'questions': questions,
        'total_questions': len(questions)
    })


### HELPER FUNCTIONS ###
def get_pending_surveys(student, all_surveys):
    date = datetime.date.today()
    day = datetime.date.isoweekday(date)
    surveys = []
    completed = []
    for s in all_surveys:
        interval_start = datetime.date
        freq = sorted(list(s.frequency))
        freq.reverse()
        for d in freq:
            if int(d) < day:
                interval_start = date - datetime.timedelta(days=day - int(d))
        else:
            interval_start = date - datetime.timedelta(days=7 - (int(d) - day))

        questions = [BooleanQuestion.objects.filter(survey=s),
                     MultipleChoiceQuestion.objects.filter(survey=s),
                     CheckboxQuestion.objects.filter(survey=s),
                     TextQuestion.objects.filter(survey=s)]

        for q in questions:
            if len(q) > 0:
                question = q[0]
                if question.question_type == "Boolean":
                    response = BooleanAnswer.objects.filter(question=question,
                                                            student__user=student)
                elif question.question_type == "Text":
                    response = TextAnswer.objects.filter(question=question,
                                                         student__user=student)
                elif question.question_type == "MultipleChoice":
                    response = MultipleChoiceAnswer.objects.filter(question=question,
                                                                   student__user=student)
                elif question.question_type == "Checkbox":
                    response = CheckboxAnswer.objects.filter(question=question,
                                                             student__user=student)

                if len(response) > 0:
                    if response.latest('timestamp').timestamp.date() < interval_start:
                        surveys.append(s)
                    else:
                        completed.append(s)
                else:
                    surveys.append(s)

                break

    return surveys, completed


def get_due_days(surveys):
    date = datetime.date.today()
    day = datetime.date.isoweekday(date)
    days_due = []
    for s in surveys:
        freq = sorted(list(s.frequency))
        due_day = int
        due_date = datetime.date
        for d in freq:
            if int(d) > day:
                due_day = int(d) - 2 if int(d) - 2 >= 0 else 6
                due_date = date - datetime.timedelta(days=7 - (int(d) - day))
                break
        else:
            due_day = int(freq[0]) - 2 if int(freq[0]) - 2 >= 0 else 6
            due_date = date - datetime.timedelta(days=day - int(d))

        if due_date > s.end_date:
            due_day = datetime.date.isoweekday(s.end_date)

        days_due.append(calendar.day_name[due_day])

    return days_due
