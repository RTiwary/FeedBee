from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.teachers.views import *
from datetime import datetime, timedelta

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request, classroom_id, survey_id):
    classroom = Classroom.objects.get(pk=classroom_id)
    survey = Survey.objects.get(pk=survey_id)
    # Structure: graph_list = [ [ title, date_labels, data ] ]
    graph_list = []

    # Don't include Base survey
    if survey.name != "Base":
        # Get all boolean questions related to survey
        boolean_questions = BooleanQuestion.objects.filter(survey_id=survey_id)

        for boolean_question in boolean_questions:
            # Get only the answers related to each boolean question
            boolean_answers = BooleanAnswer.objects.filter(question=boolean_question)

            # Only fetch data if there are responses to a question
            if len(boolean_answers) > 0:
                title = boolean_question.question_text
                boolean_date, boolean_data = display_unit_boolean_graph(survey, boolean_answers)

                # Add boolean_date and boolean_data to data package
                graph_list.append([title, boolean_date, boolean_data])

        # Get all text questions related to survey
        text_questions = TextQuestion.objects.filter(survey_id=survey)

        for text_question in text_questions:
            # Get only the answers related to each text question
            text_answers = TextAnswer.objects.filter(question=text_question)

            # Only fetch data if there are responses to a question
            if len(text_answers) > 0:
                title = text_question.question_text
                text_date, text_data = display_unit_text_graph(survey, text_answers)

                # Add text_date and text_data to data package
                graph_list.append([title, text_date, text_data])

        # Get all mc questions related to survey
        mc_questions = MultipleChoiceQuestion.objects.filter(survey_id=survey)

        for mc_question in mc_questions:
            # Get only the answers related to each mc question
            mc_answers = MultipleChoiceAnswer.objects.filter(question=mc_question)

            # Only fetch data if there are responses to a question
            if len(mc_answers) > 0:
                title = mc_question.question_text
                mc_date, mc_data = display_unit_mc_graph(survey, mc_answers)

                # Add mc_date and mc_data to data package
                graph_list.append([title, mc_date, mc_data])

        # Get all checkbox questions related to survey
        checkbox_questions = CheckboxQuestion.objects.filter(survey_id=survey)

        for checkbox_question in checkbox_questions:
            # Get only the answers related to each checkbox question
            checkbox_answers = CheckboxAnswer.objects.filter(question=checkbox_question)
            question_id = checkbox_question.id

            # Only fetch data if there are responses to a question
            if len(checkbox_answers) > 0:
                title = checkbox_question.question_text
                checkbox_date, checkbox_data = display_unit_checkbox_graph(survey, checkbox_answers, question_id)

                # Add checkbox_date and checkbox_data to data package
                graph_list.append([title, checkbox_date, checkbox_data])

    return render(request, "teachers/dashboard.html", {"graph_data": graph_list})

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
# 				backgroundColor: window.chartColors.red,
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
def display_unit_boolean_graph(survey, boolean_answers):
    # date: [number true, number responses]
    interval_data = {}

    for boolean_answer in boolean_answers:
        # Get interval date given the survey and timestamp
        interval = findInterval(survey, boolean_answer.timestamp)

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

def display_unit_text_graph(survey, text_answers):
    return [], []

def display_unit_mc_graph(survey, mc_answers):
    return [], []

def display_unit_checkbox_graph(frequency, checkbox_answers, question_id):
    # One each for all answer choices
    # date: [[number checked, number responses], [number checked, number responses], ....5 of these]
    interval_data = {}

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

    for question in interval_data.values():
        choices_percentage = []
        index = 0
        for choice in question:
            choice_element = []
            choice_title = CheckboxQuestion.objects.filter(pk=question_id).first()

            if index == 0:
                choice_element.append(choice_title.option_a)
            elif index == 1:
                choice_element.append(choice_title.option_b)
            elif index == 2:
                choice_element.append(choice_title.option_c)
            elif index == 3:
                choice_element.append(choice_title.option_d)
            elif index == 4:
                choice_element.append(choice_title.option_e)

            choice_element.append(round((float(choice[0]) / choice[1]) * 100.0))
            choices_percentage.append(choice_element)
            index += 1
        interval_percentage.append(choices_percentage)

    return interval_dates, interval_percentage

# Returns the interval (a date) that an answer belongs to given the timestamp and the survey
def findInterval(survey, timestamp):
    frequency_string = survey.frequency
    answer_date = timestamp.date()
    interval_day = answer_date
    difference = -7

    if len(frequency_string) == 1:
        difference = answer_date.isoweekday() - int(frequency_string)
    else:
        # Find most recent earlier interval date before the answer_date
        for i in range(0, len(frequency_string)):
            if answer_date.isoweekday() < int(frequency_string[i]):
                if i != 0:
                    difference = answer_date.isoweekday() - int(frequency_string[i-1])
                break

    if difference == -7:
        difference = answer_date.isoweekday() - int(frequency_string[-1])

    if difference < 0:
        difference = difference + 7

    interval_day = interval_day - timedelta(days=difference)
    return interval_day.strftime('%Y-%m-%d')
