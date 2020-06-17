from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from itertools import chain

# Create your views here.
from django.urls import reverse

from apps.students.forms import JoinClassForm
from apps.teachers.models import CheckboxQuestion, TextQuestion, BooleanQuestion, MultipleChoiceQuestion, Survey, \
    Classroom
from django.contrib.auth.decorators import login_required, user_passes_test
# test for if user is student
def is_student(user):
    return user.is_student

@login_required
@user_passes_test(is_student)
def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["class_code"]
            student = request.user.student_profile
            classroom = Classroom.objects.get(pk=code)
            classroom.students.add(student)
            return redirect("student_dashboard")

    else:
        form = JoinClassForm()

    return render(request, "students/join_class.html", {'form': form})

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    surveys = Survey.objects.filter(classroom__students__user=request.user)\
        .exclude(completed_students__user=request.user)

    return render(request, "students/dashboard.html", {
        'surveys': surveys,
        'empty': len(surveys) == 0
    })

@login_required
@user_passes_test(is_student)
def view_classes(request):
    class_list = Classroom.objects.filter(students__user=request.user)
    return render(request, "students/view_classes.html", {'class_list': class_list})

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
def take_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    baseBoolQuestions = BooleanQuestion.objects.filter(survey__name="Base").latest('creation_date')
    baseMCQuestions = MultipleChoiceQuestion.objects.filter(survey__name="Base").latest('creation_date')
    baseTxtQuestions = TextQuestion.objects.filter(survey__name="Base").latest('creation_date')
    baseCBQuestions = CheckboxQuestion.objects.filter(survey__name="Base").latest('creation_date')
    unorderedBaseQuestions = list(chain(baseBoolQuestions + baseMCQuestions + baseTxtQuestions + baseCBQuestions))
    baseQuestions = list[len(unorderedBaseQuestions)]
    for i in range(len(unorderedBaseQuestions)):
        baseQuestions[unorderedBaseQuestions[i].question_rank] = unorderedBaseQuestions[i]

    unitBoolQuestions = BooleanQuestion.objects.filter(survey=survey)
    unitMCQuestions = MultipleChoiceQuestion.objects.filter(survey=survey)
    unitTxttQuestions = TextQuestion.objects.filter(survey=survey)
    unitCBQuestions = CheckboxQuestion.object.filter(survey=survey)
    unorderedUnitQuestions = list(chain(unitBoolQuestions + unitMCQuestions + unitTxttQuestions + unitCBQuestions))
    unitQuestions = list[len(unorderedBaseQuestions)]
    for i in range(len(unorderedUnitQuestions)):
        unitQuestions[unorderedUnitQuestions[i].question_rank] = unorderedUnitQuestions[i]

    return render(request, 'templates/students/take_survey.html', {
        'survey': survey,
        'questions': list(chain(baseQuestions + unitQuestions)),
        'total_questions': len(baseQuestions) + len(unitQuestions)
    })
