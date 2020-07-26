from collections import OrderedDict
from copy import deepcopy

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.teachers.views import *
from datetime import datetime, timedelta
from collections import OrderedDict


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
    graph_list = []

    # If Base, use weekly intervals
    frequency = str
    if survey.name == "Base":
        frequency = '1'
    else:
        frequency = survey.frequency

    # Get all boolean questions related to survey
    boolean_questions = BooleanQuestion.objects.filter(survey_id=survey_id)

    for boolean_question in boolean_questions:
        # Get only the answers related to each boolean question
        boolean_answers = BooleanAnswer.objects.filter(question=boolean_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(boolean_answers) > 0:
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
            title = text_question.question_text
            text_date, text_data = display_unit_text_graph(frequency, text_answers)

            # Add text_date and text_data to data package
            graph_list.append(['text', title, text_date, text_data])

    # Get all mc questions related to survey
    mc_questions = MultipleChoiceQuestion.objects.filter(survey_id=survey)

    for mc_question in mc_questions:
        # Get only the answers related to each mc question
        mc_answers = MultipleChoiceAnswer.objects.filter(question=mc_question).order_by('timestamp')

        # Only fetch data if there are responses to a question
        if len(mc_answers) > 0:
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
            title = checkbox_question.question_text
            checkbox_date, checkbox_data = display_unit_checkbox_graph(frequency, checkbox_answers)

            # Add checkbox_date and checkbox_data to data package
            graph_list.append(['checkbox', title, checkbox_date, checkbox_data])

    return render(request, "dashboard/teacher_dashboard.html", {
        "graph_data": graph_list, 'classroom': classroom, 'curr_survey': survey, 'class_list': class_list,
        'survey_list': survey_list
    })

# Sample data format from ChartJS for line graph
#
# new Chart(document.getElementById("chartjs-0"),
#           {"type":"line","data":{"labels":["January","February","March","April","May","June","July"],
#                                  "datasets":[{"label":"My First Dataset",
#                                               "data":[65,59,80,81,56,55,40],"fill":false,
#                                               "borderColor":"rgb(75, 192, 192)",
#                                               "lineTension":0.1}]},"options":{}});

# Sample data format from ChartJS for stacked bar graph
#
# 		var barChartData = {
# 			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
# 			datasets: [{
# 				label: 'Dataset 1',
# 				data: [
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor()
# 				]
# 			}, {
# 				label: 'Dataset 2',
# 				backgroundColor: window.chartColors.blue,
# 				data: [
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor()
# 				]
# 			}, {
# 				label: 'Dataset 3',
# 				backgroundColor: window.chartColors.green,
# 				data: [
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor(),
# 					randomScalingFactor()
# 				]
# 			}]
#
# 		};


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
    return [], []


def display_unit_mc_graph(frequency, mc_answers):
    # data {
    #   interval_date: { A: num_chosen, B: num_chosen, C: num_chosen, D: num_chosen, E: num_chosen }
    # }
    data = OrderedDict()
    options = {}
    if mc_answers[0].question.option_c is None:
        options = {'A': 0, 'B': 0}
    elif mc_answers[0].question.option_d is None:
        options = {'A': 0, 'B': 0, 'C': 0}
    elif mc_answers[0].question.option_e is None:
        options = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    else:
        options = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

    for ans in mc_answers:
        # Get interval date given the survey and timestamp
        interval = findInterval(frequency, ans.timestamp)

        # Check if interval exists already in dictionary
        if interval not in data:
            data[interval] = deepcopy(options)

        data[interval][ans.answer] += 1

    # Calculate percentage for every choice for each interval
    dataset = []
    for option in options:
        option_data = {'label': option, 'data': []}
        for interval in data:
            option_data['data'].append(data[interval][option]/sum(data[interval].values()))

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
        for checked in checkbox_answer.answer:
            interval_data[interval][ord(checked) - ord('A')][0] += 1

    interval_dates = list(interval_data.keys())

    # Calculate percentages for each individual choice
    interval_percentage = []

    # Add dictionaries for each choice
    choice_title = CheckboxQuestion.objects.filter(pk=checkbox_answers[0].question.pk).first()
    interval_percentage.append({'label': choice_title.option_a, 'data': []})
    interval_percentage.append({'label': choice_title.option_b, 'data': []})
    interval_percentage.append({'label': choice_title.option_c, 'data': []})
    interval_percentage.append({'label': choice_title.option_d, 'data': []})
    interval_percentage.append({'label': choice_title.option_e, 'data': []})

    for date in interval_data.values():
        index = 0
        for choice in date:
            interval_percentage[index]['data'].append(round((float(choice[0]) / choice[1]) * 100.0))
            index += 1

    return interval_dates, interval_percentage


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
                    difference = answer_date.isoweekday() - int(frequency[i-1])
                break

    if difference == -7:
        difference = answer_date.isoweekday() - int(frequency[-1])

    if difference < 0:
        difference = difference + 7

    interval_day = interval_day - timedelta(days=difference)
    return interval_day.strftime('%Y-%m-%d')
