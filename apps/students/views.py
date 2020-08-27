import calendar
import datetime
import operator

from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from itertools import chain
from django.http import Http404
from django.urls import reverse
from apps.users.models import *
from apps.students.models import CheckboxAnswer, TextAnswer, BooleanAnswer, MultipleChoiceAnswer
from apps.teachers.models import CheckboxQuestion, TextQuestion, BooleanQuestion, MultipleChoiceQuestion, Survey, \
    Classroom
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from .forms import *
from pytz import timezone
from datetime import datetime as timezonedate

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
            classroom = get_object_or_404(Classroom, pk=code)
            classroom.students.add(student)
            return redirect("student_dashboard")
    elif classroom_id is not None and int(classroom_id) >= 0:
        form = JoinClassForm(initial={"class_code": classroom_id})
        try:
            classroom_name = get_object_or_404(Classroom, pk=int(classroom_id)).name
        except Exception:
            classroom_name = " "
        return render(request, "students/join_class.html", {'form': form, 'classroom_name': classroom_name})

    form = JoinClassForm()
    return render(request, "students/join_class.html", {'form': form})


@login_required
@user_passes_test(is_student)
def leave_class(request, classroom_id):
    student = request.user.student_profile
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    # check if student is in the classroom
    if student not in classroom.students.all():
        raise Http404

    classroom.students.remove(student)
    return redirect(student_dashboard)


# displays all pending surveys to student
@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    # Query for all surveys except Base and expired surveys
    all_surveys = Survey.objects.filter(classroom__students__user=request.user) \
        .exclude(name="Base").exclude(end_date__lte=timezonedate.now(timezone('US/Eastern')).date())

    # Remove surveys that have already been completed for this interval
    surveys, filler = get_pending_surveys(request.user, all_surveys)
    # Get due date for each survey
    days_due = get_due_days(surveys)

    return render(request, "students/dashboard.html", {
        'surveys': zip(surveys, days_due),
        'empty': len(surveys) == 0
    })


# allows student to view all of their classes + each class's teacher name
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

    # class list is a list of all classes and the names of their respective teachers
    class_list = zip(classes, teachers)
    return render(request, "students/view_classes.html", {'class_list': class_list})


# allows students to view all of their surveys by returning lists for both completed and not completed surveys
@login_required
@user_passes_test(is_student)
def view_surveys(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    student = request.user.student_profile

    # check if student is in the classroom
    if student not in classroom.students.all():
        raise Http404

    all_surveys = Survey.objects.filter(classroom=classroom) \
        .exclude(name="Base").exclude(end_date__lte=timezonedate.now(timezone('US/Eastern')).date())

    surveys, completed = get_pending_surveys(request.user, all_surveys)
    days_due = get_due_days(surveys)

    lists_empty = False
    if not surveys and not completed:
        lists_empty = True

    return render(request, "students/view_surveys.html", {'classroom': classroom,
                                                          'surveys': zip(surveys, days_due),
                                                          'completed': completed,
                                                          'lists_empty': lists_empty})


@login_required
@user_passes_test(is_student)
def suggest_feature(request):
    if request.method == 'POST':
        form = SuggestFeatureForm(request.POST)
        if form.is_valid():
            # Send suggestion to inbox
            send_mail(
                'FeedBee: {}'.format(form.cleaned_data['comment_type_choice']),
                "A user wrote the following:\n\n" + form.cleaned_data['comment'],
                None,
                ['classbopteam@gmail.com'],
                fail_silently=False,
            )
            return render(request, "students/suggest_feature.html", {'form': SuggestFeatureForm(), 'toast': "1"})

    form = SuggestFeatureForm()
    return render(request, "students/suggest_feature.html", {'form': form, 'toast': "-1"})


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
    classroom = get_object_or_404(Classroom, pk=survey.classroom.id)

    # check if student is in the classroom
    if student not in classroom.students.all():
        raise Http404

    # Query for class base questions and place into list sorted by question_rank
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

    # Query for survey questions and place into list sorted by question_rank
    unit_bool_questions = BooleanQuestion.objects.filter(survey=survey)
    unit_mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey)
    unit_txt_questions = TextQuestion.objects.filter(survey=survey)
    unit_cb_questions = CheckboxQuestion.objects.filter(survey=survey)
    unit_questions = \
        list(chain(unit_bool_questions, unit_mc_questions, unit_txt_questions, unit_cb_questions))
    unit_questions = sorted(unit_questions, key=operator.attrgetter('question_rank'))

    questions = list(chain(unit_questions, base_questions))

    # If survey submitted, save responses
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


# HELPER FUNCTIONS
# filters out surveys that have already been submitted for the current interval
def get_pending_surveys(student, all_surveys):
    eastern = timezone('US/Eastern')
    date = timezonedate.now(eastern).date()
    day = datetime.date.isoweekday(date)
    pending = []
    completed = []
    for s in all_surveys:
        # Find start date of current interval
        interval_start = datetime.date

        # Iterate backwards through frequency and find first day that comes before today
        freq = sorted(list(s.frequency))
        freq.reverse()
        for d in freq:
            if int(d) <= day:
                interval_start = date - datetime.timedelta(days=day - int(d))
                break

        # If no day before today in frequency, choose last day in frequency(from the week before)
        else:
            interval_start = date - datetime.timedelta(days=7 - (int(freq[0]) - day))

        questions = [BooleanQuestion.objects.filter(survey=s),
                     MultipleChoiceQuestion.objects.filter(survey=s),
                     CheckboxQuestion.objects.filter(survey=s),
                     TextQuestion.objects.filter(survey=s)]

        # Check if student responded since start of current interval
        for q in questions:
            # Query for a question from the survey
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

                # If student has never responded or has not responded in this interval,
                # it is pending, else it is completed
                if len(response) > 0:
                    if response.latest('timestamp').timestamp.date() < interval_start:
                        pending.append(s)
                    else:
                        completed.append(s)
                else:
                    pending.append(s)

                break

    return pending, completed


# Get due date for surveys based on frequencies
def get_due_days(surveys):
    eastern = timezone('US/Eastern')
    date = timezonedate.now(eastern).date()
    day = datetime.date.isoweekday(date)
    days_due = []
    for s in surveys:
        # Find first day after today in frequency
        freq = sorted(list(s.frequency))
        due_day = int
        due_date = datetime.date
        for d in freq:
            if int(d) > day:
                due_day = int(d) - 2 if int(d) - 2 >= 0 else 6
                due_date = date - datetime.timedelta(days=7 - (int(d) - day))
                break

        # If no day after today, use the first day of next week
        else:
            due_day = int(freq[0]) - 2 if int(freq[0]) - 2 >= 0 else 6
            due_date = date - datetime.timedelta(days=day - int(freq[0]))

        # If end of current interval is passed end date, due date is the end date
        if due_date > s.end_date:
            due_day = datetime.date.isoweekday(s.end_date)

        days_due.append(calendar.day_name[due_day])

    return days_due
