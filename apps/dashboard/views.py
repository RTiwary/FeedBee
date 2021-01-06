import datetime
from copy import deepcopy
from apps.teachers.views import *
from collections import OrderedDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta

# tests if user is teacher
def is_teacher(user):
    return user.is_teacher


@login_required
@user_passes_test(is_teacher)
def dash(request):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)

    # return list of the teacher's classrooms
    return render(request, "dashboard/dash_select_class.html", {'class_list': class_list})


'''allows teacher to select the survey they want given they already select the classroom'''


@login_required
@user_passes_test(is_teacher)
def dash_select(request, classroom_id):
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    classroom = Classroom.objects.get(pk=classroom_id)
    survey_list = Survey.objects.filter(classroom_id=classroom_id)
    # returns list of the surveys in the selected classroom
    return render(request, "dashboard/dash_select_survey.html", {
        'classroom': classroom, 'class_list': class_list, 'survey_list': survey_list
    })


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request, classroom_id, survey_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    survey = Survey.objects.get(pk=survey_id)
    teacher = request.user.teacher_profile
    class_list = Classroom.objects.filter(teacher_id=teacher.id)
    survey_list = Survey.objects.filter(classroom_id=classroom_id)

    # Structure: graph_list = [ [ graph_type, title, date_labels, data ] ]
    # Graph items for True/False: title, date_labels, data
    # Graph items for Text: [type, title, responselist (ordereddict) ]
    # ex: { date1: [response1, response2], date2: [response3, response4] }
    graph_list = []

    # If Base, use weekly intervals
    frequency = str
    if survey.name == "Base":
        frequency = '1'
    else:
        frequency = survey.frequency
        graph_list = [['boolean', 'Response Rate']]

    # Get all boolean questions related to survey
    boolean_questions = BooleanQuestion.objects.filter(survey_id=survey_id)

    for boolean_question in boolean_questions:
        # Get only the answers related to each boolean question
        boolean_answers = BooleanAnswer.objects.filter(question=boolean_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(boolean_answers) > 0:
            if survey.name != 'Base':
                graph_list[0].extend(display_response_rate_graph(survey, boolean_answers))

            title = boolean_question.question_text
            boolean_date, boolean_data = display_unit_boolean_graph(frequency, boolean_answers)

            # Add boolean_date and boolean_data to data package
            graph_list.append(['boolean', title, boolean_date, boolean_data])

    # Get all text questions related to survey
    text_questions = TextQuestion.objects.filter(survey_id=survey)

    for text_question in text_questions:
        # Get only the answers related to each text question
        text_answers = TextAnswer.objects.filter(question=text_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(text_answers) > 0:
            if survey.name != 'Base' and len(graph_list[0]) == 2:
                graph_list[0].extend(display_response_rate_graph(survey, text_answers))

            title = text_question.question_text
            responses_list = display_unit_text_graph(frequency, text_answers)

            # Add text_date and text_data to data package
            graph_list.append(['text', title, responses_list])

    # Get all mc questions related to survey
    mc_questions = MultipleChoiceQuestion.objects.filter(survey_id=survey)

    for mc_question in mc_questions:
        # Get only the answers related to each mc question
        mc_answers = MultipleChoiceAnswer.objects.filter(question=mc_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(mc_answers) > 0:
            if survey.name != 'Base' and len(graph_list[0]) == 2:
                graph_list[0].extend(display_response_rate_graph(survey, mc_answers))

            title = mc_question.question_text
            mc_date, mc_data = display_unit_mc_graph(frequency, mc_answers)

            # Add mc_date and mc_data to data package
            graph_list.append(['mc', title, mc_date, mc_data])

    # Get all checkbox questions related to survey
    checkbox_questions = CheckboxQuestion.objects.filter(survey_id=survey)

    for checkbox_question in checkbox_questions:
        # Get only the answers related to each checkbox question
        checkbox_answers = CheckboxAnswer.objects.filter(question=checkbox_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(checkbox_answers) > 0:
            if survey.name != 'Base' and len(graph_list[0]) == 2:
                graph_list[0].extend(display_response_rate_graph(survey, checkbox_answers))

            title = checkbox_question.question_text
            checkbox_date, checkbox_data = display_unit_checkbox_graph(frequency, checkbox_answers)

            # Add checkbox_date and checkbox_data to data package
            graph_list.append(['checkbox', title, checkbox_date, checkbox_data])

    return render(request, "dashboard/teacher_dashboard.html", {
        "graph_data": graph_list, 'classroom': classroom, 'curr_survey': survey, 'class_list': class_list,
        'survey_list': survey_list
    })


# Returns data needed to display boolean graph
def display_unit_boolean_graph(frequency, boolean_answers):
    # date: [number true, number responses]
    interval_data = OrderedDict()

    for boolean_answer in boolean_answers:
        # Get interval date given the survey and timestamp
        interval = findInterval(frequency, boolean_answer.timestamp)

        # Check if interval exists already in dictionary
        if interval in interval_data:
            interval_data[interval][1] += 1
        else:
            interval_data[interval] = [0, 1]

        # Increment if True
        if boolean_answer.answer:
            interval_data[interval][0] += 1

    interval_dates = list(interval_data.keys())
    interval_percentage = list(round((float(pair[0]) / pair[1]) * 100.0) for pair in interval_data.values())
    return interval_dates, interval_percentage


def display_unit_text_graph(frequency, text_answers):
    responses_list = OrderedDict()
    for text_answer in text_answers:
        interval = findInterval(frequency, text_answer.timestamp)

        # check if interval already exists in responses_list
        if interval in responses_list:
            responses_list[interval].append(text_answer.answer)
        else:
            responses_list[interval] = [text_answer.answer]

    return responses_list


def display_unit_mc_graph(frequency, mc_answers):
    # data {
    #   interval_date: { A: num_chosen, B: num_chosen, C: num_chosen, D: num_chosen, E: num_chosen }
    # }
    data = OrderedDict()
    options = OrderedDict()

    if mc_answers[0].question.option_c is None:
        options = {mc_answers[0].question.option_a: 0, mc_answers[0].question.option_b: 0}
    elif mc_answers[0].question.option_d is None:
        options = {mc_answers[0].question.option_a: 0, mc_answers[0].question.option_b: 0, mc_answers[0].question.option_c: 0}
    elif mc_answers[0].question.option_e is None:
        options = {mc_answers[0].question.option_a: 0, mc_answers[0].question.option_b: 0, mc_answers[0].question.option_c: 0, mc_answers[0].question.option_d: 0}
    else:
        options = {mc_answers[0].question.option_a: 0, mc_answers[0].question.option_b: 0, mc_answers[0].question.option_c: 0, mc_answers[0].question.option_d: 0, mc_answers[0].question.option_e: 0}

    for ans in mc_answers:
        # Get interval date given the survey and timestamp
        interval = findInterval(frequency, ans.timestamp)

        # Check if interval exists already in dictionary
        if interval not in data:
            data[interval] = deepcopy(options)

        if ans.answer == 'A':
            data[interval][mc_answers[0].question.option_a] += 1
        elif ans.answer == 'B':
            data[interval][mc_answers[0].question.option_b] += 1
        elif ans.answer == 'C':
            data[interval][mc_answers[0].question.option_c] += 1
        elif ans.answer == 'D':
            data[interval][mc_answers[0].question.option_d] += 1
        else:
            data[interval][mc_answers[0].question.option_e] += 1

    # Calculate percentage for every choice for each interval
    dataset = []
    for option in options:
        option_data = {'label': option, 'data': []}
        for interval in data:
            option_data['data'].append(round((data[interval][option] / sum(data[interval].values())) * 100))

        dataset.append(option_data)

    # Interval dates(labels) and answer percentages for each interval
    return list(data.keys()), dataset


def display_unit_checkbox_graph(frequency, checkbox_answers):
    # date: [[number checked, number responses], [number checked, number responses], ....5 of these for each choice]
    interval_data = OrderedDict()

    for checkbox_answer in checkbox_answers:
        # Get interval date given the survey and timestamp
        interval = findInterval(frequency, checkbox_answer.timestamp)

        # Check if interval doesn't exist in dictionary
        if interval not in interval_data:
            interval_data[interval] = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

        # Increment responses for all choices
        for i in range(5):
            interval_data[interval][i][1] += 1

        # Increment if True
        if checkbox_answer.answer:
            for checked in checkbox_answer.answer:
                interval_data[interval][ord(checked) - ord('A')][0] += 1

    interval_dates = list(interval_data.keys())

    # Calculate percentages for each individual choice
    interval_percentage = []

    # Add dictionaries for each choice
    choice_title = CheckboxQuestion.objects.filter(pk=checkbox_answers[0].question.pk).first()
    interval_percentage.append({'label': choice_title.option_a, 'data': []})

    if choice_title.option_b is not None:
        interval_percentage.append({'label': choice_title.option_b, 'data': []})

    if choice_title.option_c is not None:
        interval_percentage.append({'label': choice_title.option_c, 'data': []})

    if choice_title.option_d is not None:
        interval_percentage.append({'label': choice_title.option_d, 'data': []})

    if choice_title.option_e is not None:
        interval_percentage.append({'label': choice_title.option_e, 'data': []})

    for date in interval_data.values():
        for index in range(len(interval_percentage)):
            interval_percentage[index]['data'].append(round((float(date[index][0]) / date[index][1]) * 100.0))

    return interval_dates, interval_percentage


# def display_response_rate_graph(survey, start_date, question_type, question_pk):
#     interval_dates = []
#     start_day = datetime.datetime(*[int(item) for item in findInterval(survey.frequency, start_date).split('-')]) \
#         .isoweekday()
#     for day in survey.frequency:
#         day = int(day)
#         if start_day > day:
#             interval_dates.append((start_date + timedelta(days=7 - (start_day - day))).date())
#         else:
#             interval_dates.append((start_date + timedelta(days=start_day - day)).date())
#
#         while (interval_dates[-1] + datetime.timedelta(days=7)) <= survey.end_date and \
#                 (interval_dates[-1] + datetime.timedelta(days=7)) <= datetime.date.today():
#             interval_dates.append(interval_dates[-1] + timedelta(days=7))
#
#     if interval_dates[-1] != survey.end_date and survey.end_date <= datetime.date.today():
#         interval_dates.append(survey.end_date)
#     interval_dates.append(survey.end_date + timedelta(days=1))
#     interval_dates.sort()
#
#     interval_response_rates = []
#     for i in range(len(interval_dates) - 1):
#         if question_type == 'boolean':
#             interval_response_rates.append((len(BooleanAnswer.objects.filter(question=question_pk)
#                                                 .exclude(timestamp__lt=interval_dates[i])
#                                                 .exclude(timestamp__gte=interval_dates[i + 1]))
#                                             / survey.classroom.students.count()) * 100)
#         elif question_type == 'text':
#             interval_response_rates.append((len(TextAnswer.objects.filter(question=question_pk)
#                                                 .exclude(timestamp__lt=interval_dates[i])
#                                                 .exclude(timestamp__gte=interval_dates[i + 1]))
#                                             / survey.classroom.students.count()) * 100)
#         elif question_type == 'mc':
#             interval_response_rates.append((len(MultipleChoiceAnswer.objects.filter(question=question_pk)
#                                                 .exclude(timestamp__lt=interval_dates[i])
#                                                 .exclude(timestamp__gte=interval_dates[i + 1]))
#                                             / survey.classroom.students.count()) * 100)
#         elif question_type == 'checkbox':
#             interval_response_rates.append((len(CheckboxAnswer.objects.filter(question=question_pk)
#                                                 .exclude(timestamp__lt=interval_dates[i])
#                                                 .exclude(timestamp__gte=interval_dates[i + 1]))
#                                             / survey.classroom.students.count()) * 100)
#
#     interval_dates.pop()
#     return interval_dates, interval_response_rates


def display_response_rate_graph(survey, responses):
    intervals = OrderedDict()

    for r in responses:
        # Get interval date given the survey and timestamp
        interval = findInterval(survey.frequency, r.timestamp)

        # Check if interval exists already in dictionary
        if interval not in intervals:
            intervals[interval] = 0

        intervals[interval] += 1

    for interval in intervals.keys():
        intervals[interval] = round(intervals[interval]/survey.classroom.students.count() * 100)

    return list(intervals.keys()), list(intervals.values())


# Returns the interval (a date) that an answer belongs to given the timestamp and the survey
def findInterval(frequency, timestamp):
    answer_date = timestamp.date()
    interval_day = answer_date
    difference = -7

    if len(frequency) == 1:
        difference = answer_date.isoweekday() - int(frequency)
    else:
        # Find most recent earlier interval date before the answer_date
        for i in range(0, len(frequency)):
            if answer_date.isoweekday() < int(frequency[i]):
                if i != 0:
                    difference = answer_date.isoweekday() - int(frequency[i - 1])
                break

    if difference == -7:
        difference = answer_date.isoweekday() - int(frequency[-1])

    if difference < 0:
        difference = difference + 7

    interval_day = interval_day - timedelta(days=difference)
    return interval_day.strftime('%m/%d/%y')
