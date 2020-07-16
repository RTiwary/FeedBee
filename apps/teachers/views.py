from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from .forms import *
from apps.teachers.models import *
from apps.students.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from itertools import chain
import operator


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

'''
Deletes a classroom in the database using the 
classroom_id and redirects to the view_classes screen
'''
@login_required
@user_passes_test(is_teacher)
def delete_class(request, classroom_id):
    # Query for classroom using classroom_id and delete that classroom
    classroom = Classroom.objects.get(pk=classroom_id)
    classroom.delete()
    return redirect("view_classes")


@login_required
@user_passes_test(is_teacher)
def choose_question_type(request, survey_id):
    # for the breadcrumb to know whether to display view recurring questions or view questions
    survey = Survey.objects.get(pk=survey_id)
    if survey.name == "Base":
        question_format = "Recurring"
    else:
        question_format = ""

    if request.method == 'POST':
        form = QuestionTypeForm(request.POST)
        if form.is_valid():
            question_type_choice = form.cleaned_data["question_type_choice"]
            if question_type_choice == "Boolean":
                return redirect("add_boolean_question", survey_id=survey_id)
            elif question_type_choice == "Text":
                return redirect("add_text_question", survey_id=survey_id)
            elif question_type_choice == "MultipleChoice":
                return redirect("add_mc_question", survey_id=survey_id)
            elif question_type_choice == "Checkbox":
                return redirect("add_checkbox_question", survey_id=survey_id)

    else:
        form = QuestionTypeForm()
    return render(request, "teachers/choose_question_type.html", {'form': form, 'survey': survey,
                                                                  'question_format': question_format})


@login_required
@user_passes_test(is_teacher)
def add_boolean_question(request, survey_id, question_id=-1):  # question_id is an optional parameter
    survey = Survey.objects.get(pk=survey_id)

    # for the breadcrumb to know whether to display view recurring questions or view questions
    if survey.name == "Base":
        question_format = "Recurring"
    else:
        question_format = ""

    if request.method == 'POST':
        if question_id < 0:
            form = BooleanQuestionForm(request.POST)
        else:
            existingQuestion = BooleanQuestion.objects.get(pk=question_id)
            form = BooleanQuestionForm(request.POST, instance=existingQuestion)

        boolean_question = form.save(commit=False)
        if form.is_valid():
            if question_id < 0:
                boolean_question.survey = survey
                objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                                survey.mc_questions.count() + survey.checkbox_questions.count()
                boolean_question.question_rank = objects_count + 1
                boolean_question.save()

            boolean_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)

    else:
        if question_id >= 0:
            existingQuestion = BooleanQuestion.objects.get(pk=question_id)
            form = BooleanQuestionForm(instance=existingQuestion)
            action = "Update"  # for the header and button text
        else:
            form = BooleanQuestionForm()
            action = "Add"

    return render(request, "teachers/add_boolean_question.html", {'form': form, 'survey': survey, 'action': action,
                                                                  'question_format': question_format})


@login_required
@user_passes_test(is_teacher)
def add_text_question(request, survey_id, question_id=-1):
    survey = Survey.objects.get(pk=survey_id)

    # for the breadcrumb to know whether to display view recurring questions or view questions
    if survey.name == "Base":
        question_format = "Recurring"
    else:
        question_format = ""

    if request.method == 'POST':
        if question_id < 0:
            form = TextQuestionForm(request.POST)
        else:
            existingQuestion = TextQuestion.objects.get(pk=question_id)
            form = TextQuestionForm(request.POST, instance=existingQuestion)

        text_question = form.save(commit=False)  # commit=False means get the obj w/o saving to the DB
        if form.is_valid():
            if question_id < 0:
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
        if question_id >= 0:
            existingQuestion = TextQuestion.objects.get(pk=question_id)
            form = TextQuestionForm(instance=existingQuestion)
            action = "Update"  # for the header and button text
        else:
            form = TextQuestionForm()
            action = "Add"
    return render(request, "teachers/add_text_question.html", {'form': form, 'survey': survey, 'action': action,
                                                               'question_format': question_format})


@login_required
@user_passes_test(is_teacher)
def add_mc_question(request, survey_id, question_id=-1):
    survey = Survey.objects.get(pk=survey_id)

    # for the breadcrumb to know whether to display view recurring questions or view questions
    if survey.name == "Base":
        question_format = "Recurring"
    else:
        question_format = ""

    if request.method == 'POST':
        if question_id < 0:
            form = MultipleChoiceQuestionForm(request.POST)
        else:
            existingQuestion = MultipleChoiceQuestion.objects.get(pk=question_id)
            form = MultipleChoiceQuestionForm(request.POST, instance=existingQuestion)

        mc_question = form.save(commit=False)
        if form.is_valid():
            if question_id < 0:
                mc_question.survey = survey
                objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                                survey.mc_questions.count() + survey.checkbox_questions.count()
                mc_question.question_rank = objects_count + 1

            mc_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)
    else:
        if question_id >= 0:
            existingQuestion = MultipleChoiceQuestion.objects.get(pk=question_id)
            form = MultipleChoiceQuestionForm(instance=existingQuestion)
            action = "Update"  # for the header and button text
        else:
            form = MultipleChoiceQuestionForm()
            action = "Add"
    return render(request, "teachers/add_mc_question.html", {'form': form, 'survey': survey, 'action': action,
                                                             'question_format': question_format})


@login_required
@user_passes_test(is_teacher)
def add_checkbox_question(request, survey_id, question_id=-1):
    survey = Survey.objects.get(pk=survey_id)

    # for the breadcrumb to know whether to display view recurring questions or view questions
    if survey.name == "Base":
        question_format = "Recurring"
    else:
        question_format = ""

    if request.method == 'POST':
        if question_id < 0:
            form = CheckboxQuestionForm(request.POST)
        else:
            existingQuestion = CheckboxQuestion.objects.get(pk=question_id)
            form = CheckboxQuestionForm(request.POST, instance=existingQuestion)

        checkbox_question = form.save(commit=False)
        if form.is_valid():
            if question_id < 0:
                checkbox_question.survey = survey
                objects_count = survey.boolean_questions.count() + survey.text_questions.count() + \
                                survey.mc_questions.count() + survey.checkbox_questions.count()
                checkbox_question.question_rank = objects_count + 1

            checkbox_question.save()
            classroom_id = survey.classroom.pk
            if survey.name == "Base":
                return redirect("view_recurring_questions", classroom_id=classroom_id)
            else:
                return redirect("view_questions", survey_id=survey_id)
    else:
        if question_id >= 0:
            existingQuestion = CheckboxQuestion.objects.get(pk=question_id)
            form = CheckboxQuestionForm(instance=existingQuestion)
            action = "Update"  # for the header and button text
        else:
            form = CheckboxQuestionForm()
            action = "Add"

    return render(request, "teachers/add_checkbox_question.html", {'form': form, 'survey': survey, 'action': action,
                                                                   'question_format': question_format})


'''
allows teacher to "delete" a question (both recurring and unit questions), removes unit questions from database but
doesn't actually delete the recurring questions (hides the question using the display field),
decrements the rank for all questions with higher rank than the one to be deleted 
'''
@login_required
@user_passes_test(is_teacher)
def delete_question(request, survey_id, question_id, type_id, classroom_id=-1):
    if type_id == "Boolean":
        question = BooleanQuestion.objects.filter(pk=question_id, survey=survey_id)
    elif type_id == "Text":
        question = TextQuestion.objects.filter(pk=question_id, survey=survey_id)
    elif type_id == "MultipleChoice":
        question = MultipleChoiceQuestion.objects.filter(pk=question_id, survey=survey_id)
    elif type_id == "Checkbox":
        question = CheckboxQuestion.objects.filter(pk=question_id, survey=survey_id)

    # Query for all questions with higher rank than the one to be deleted and decrement
    question_rank = question[0].question_rank
    boolean_questions = BooleanQuestion.objects.filter(question_rank__gt=question_rank, survey=survey_id)
    text_questions = TextQuestion.objects.filter(question_rank__gt=question_rank, survey=survey_id)
    mc_questions = MultipleChoiceQuestion.objects.filter(question_rank__gt=question_rank, survey=survey_id)
    checkbox_questions = CheckboxQuestion.objects.filter(question_rank__gt=question_rank, survey=survey_id)
    question_list = list(chain(boolean_questions, text_questions, mc_questions, checkbox_questions))

    for questionDecrement in question_list:
        questionDecrement.question_rank = questionDecrement.question_rank - 1
        questionDecrement.save()

    survey = Survey.objects.get(pk=survey_id)

    # if recurring question, update the display field to 'False', otherwise just delete
    if survey.name == "Base":
        question.update(display=False)
        classroom_id = survey.classroom.pk
        return redirect("view_recurring_questions", classroom_id=classroom_id)
    else:
        question.delete()
        return redirect("view_questions", survey_id=survey_id)


@login_required
@user_passes_test(is_teacher)
def view_classes(request):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    return render(request, "teachers/view_classes.html", {'class_list': class_list})


@login_required
@user_passes_test(is_teacher)
def view_questions(request, survey_id):
    if request.method == 'POST':
        survey = Survey.objects.get(pk=survey_id)
        form = SurveyEditForm(request.POST, initial={'survey_name': survey.name, 'end_date': survey.end_date})
        if form.is_valid():
            new_name = form.cleaned_data["survey_name"]
            new_end_date = form.cleaned_data["end_date"]
            survey.name = new_name
            survey.end_date = new_end_date
            survey.save()
    else:
        survey = Survey.objects.get(pk=survey_id)
        form = SurveyEditForm(initial={'survey_name': survey.name, 'end_date': survey.end_date})

    frequency_mapping = {"1":"Monday", "2":"Tuesday", "3":"Wednesday", "4":"Thursday", "5":"Friday", "6":"Saturday",
                         "7":"Sunday"}
    frequency_list = []
    for number in survey.frequency:
        frequency_list.append(frequency_mapping[number])

    boolean_questions = BooleanQuestion.objects.filter(survey=survey_id)
    text_questions = TextQuestion.objects.filter(survey=survey_id)
    mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey_id)
    checkbox_questions = CheckboxQuestion.objects.filter(survey=survey_id)
    question_list = list(chain(boolean_questions, text_questions, mc_questions, checkbox_questions))
    question_list = sorted(question_list, key=operator.attrgetter('question_rank'))

    return render(request, "teachers/view_questions.html", {'form': form, "frequency_list": frequency_list,
                                                            "questions": question_list, "survey": survey})


@login_required
@user_passes_test(is_teacher)
def view_recurring_questions(request, classroom_id):
    base_survey_queryset = Survey.objects.filter(name="Base").filter(classroom_id=classroom_id)
    if not base_survey_queryset:
        survey_classroom = Classroom.objects.get(id=classroom_id)
        baseSurvey = Survey.objects.create(name="Base", classroom=survey_classroom)
    else:
        baseSurvey = base_survey_queryset[0]
    recurring_boolean_questions = BooleanQuestion.objects.filter(survey=baseSurvey, display=True)
    recurring_text_questions = TextQuestion.objects.filter(survey=baseSurvey, display=True)
    recurring_mc_questions = MultipleChoiceQuestion.objects.filter(survey=baseSurvey, display=True)
    recurring_checkbox_questions = CheckboxQuestion.objects.filter(survey=baseSurvey, display=True)
    recurring_question_list = list(chain(recurring_boolean_questions, recurring_text_questions, recurring_mc_questions,
                                         recurring_checkbox_questions))
    recurring_question_list = sorted(recurring_question_list, key=operator.attrgetter('question_rank'))
    return render(request, "teachers/view_recurring_questions.html", {"questions": recurring_question_list,
                                                                      "base_survey_id": baseSurvey.pk,
                                                                      "classroom_id": classroom_id})


'''
allows teacher to add a new survey using the form, adds new survey into database, redirects them to view_questions page
'''
@login_required
@user_passes_test(is_teacher)
def add_survey(request, classroom_id):
    if request.method == 'POST':
        form = SurveyCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["survey_name"]
            end_date = form.cleaned_data["end_date"]
            frequency_list = form.cleaned_data["frequency"]
            frequency = ""
            for day in frequency_list:
                frequency += day
            new_survey = Survey.objects.create(name=name, end_date=end_date, frequency=frequency,
                                               classroom_id=classroom_id)
            return redirect("view_questions", survey_id=new_survey.id)

    else:
        form = SurveyCreationForm()

    return render(request, "teachers/add_survey.html", {'form': form, "classroom_id": classroom_id})


'''allows teacher to delete a survey, removes the survey from the database and redirects them to view_classroom_info'''
@login_required
@user_passes_test(is_teacher)
def delete_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    classroom = Classroom.objects.get(pk=survey.classroom.pk)
    survey.delete()
    return redirect("view_classroom_info", classroom_id=classroom.pk)


'''
gets the info for teacher to view the results/answers of a survey, returns a dictionary with each question as a key
and a list of answers as a value
'''
@login_required
@user_passes_test(is_teacher)
def view_results(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)

    # Queries for all of the questions in the survey and sort them based on rank
    boolean_questions = BooleanQuestion.objects.filter(survey=survey_id)
    text_questions = TextQuestion.objects.filter(survey=survey_id)
    mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey_id)
    checkbox_questions = CheckboxQuestion.objects.filter(survey=survey_id)
    question_list = list(chain(boolean_questions, text_questions, mc_questions, checkbox_questions))
    question_list = sorted(question_list, key=operator.attrgetter('question_rank'))

    # For each survey question, query the answers to each question as a list of values
    answers = []
    for question in question_list:
        if question.question_type == "Boolean":
            answer = BooleanAnswer.objects.filter(question=question).values_list('answer', flat=True)
        elif question.question_type == "Text":
            answer = TextAnswer.objects.filter(question=question).values_list('answer', flat=True)
        elif question.question_type == "MultipleChoice":
            answer = MultipleChoiceAnswer.objects.filter(question=question).values_list('answer', flat=True)
        elif question.question_type == "Checkbox":
            answer = CheckboxAnswer.objects.filter(question=question).values_list('answer', flat=True)

        answers.append(answer)

    # returns a dictionary with each question as the key and a corresponding list of answers as the values
    q_and_a = dict(zip(question_list, answers))

    return render(request, "teachers/view_results.html", {"survey": survey,
                                                          'q_and_a': q_and_a})

@login_required
@user_passes_test(is_teacher)
def view_results_alt(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    classroom = survey.classroom

    boolean_questions = BooleanQuestion.objects.filter(survey=survey_id)
    text_questions = TextQuestion.objects.filter(survey=survey_id)
    mc_questions = MultipleChoiceQuestion.objects.filter(survey=survey_id)
    checkbox_questions = CheckboxQuestion.objects.filter(survey=survey_id)
    question_list = list(chain(boolean_questions, text_questions, mc_questions, checkbox_questions))
    question_list = sorted(question_list, key=operator.attrgetter('question_rank'))

    answers_table = []
    for student in classroom.students.all():
        answers = []
        for question in question_list:
            if question.question_type == "Boolean":
                answers.append(BooleanAnswer.objects.filter(question=question, student=student)\
                               .values_list('answer', flat=True)[0])
            if question.question_type == "Text":
                answers.append(TextAnswer.objects.filter(question=question, student=student)\
                               .values_list('answer', flat=True)[0])
            if question.question_type == "MultipleChoice":
                a = MultipleChoiceAnswer.objects.filter(question=question, student=student)\
                    .values_list('answer', flat=True)[0]
                if a == "A":
                    answers.append(question.option_a)
                elif a == "B":
                    answers.append(question.option_b)
                elif a == "C":
                    answers.append(question.option_c)
                elif a == "D":
                    answers.append(question.option_d)
                elif a == "E":
                    answers.append(question.option_e)
            if question.question_type == "Checkbox":
                a = CheckboxAnswer.objects.filter(question=question, student=student)\
                    .values_list('answer', flat=True)[0]
                chosen = ""
                if a == "":
                    chosen = "None"
                if "A" in a:
                    chosen = question.option_a
                if "B" in a:
                    if chosen == "":
                        chosen = question.option_b
                    else:
                        chosen = chosen + ", " + question.option_b
                if "C" in a:
                    if chosen == "":
                        chosen = question.option_c
                    else:
                        chosen = chosen + ", " + question.option_c
                if "D" in a:
                    if chosen == "":
                        chosen = question.option_d
                    else:
                        chosen = chosen + ", " + question.option_d
                if "E" in a:
                    if chosen == "":
                        chosen = question.option_e
                    else:
                        chosen = chosen + ", " + question.option_e
                answers.append(chosen)

        answers_table.append(answers)

    return render(request, "teachers/view_results_alt.html", {"survey": survey,
                                                              "questions": question_list,
                                                              "answers": answers_table})


@login_required
@user_passes_test(is_teacher)
def view_classroom_info(request, classroom_id):
    if request.method == 'POST':
        classroom = Classroom.objects.get(pk=classroom_id)
        form = ClassroomEditForm(request.POST, initial={'class_name': classroom.name})
        if form.is_valid():
            new_name = form.cleaned_data["class_name"]
            classroom.name = new_name
            classroom.save()
    else:
        classroom = Classroom.objects.get(pk=classroom_id)
        form = ClassroomEditForm(initial={'class_name': classroom.name})
    surveys = Survey.objects.filter(classroom_id=classroom_id).exclude(name="Base")
    return render(request, "teachers/view_classroom_info.html",
                  {'form': form, 'classroom': classroom, 'surveys': surveys})


@login_required
@user_passes_test(is_teacher)
def suggest_feature(request):
    return render(request, "teachers/suggest_feature.html")


@login_required
@user_passes_test(is_teacher)
def logout_request(request):
    logout(request)
    return redirect(reverse("homepage"))
