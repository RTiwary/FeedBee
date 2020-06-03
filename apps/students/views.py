from django.shortcuts import render, get_object_or_404


# Create your views here.
from apps.teachers.models import CheckboxQuestion, TextQuestion, BooleanQuestion, MultipleChoiceQuestion, Survey


def take_quiz(request, pk):
    quiz = get_object_or_404(Survey, pk=pk)
    student = request.user.student

    boolQuestions = BooleanQuestion.objects.filter(quiz=quiz)
    mcQuestions = MultipleChoiceQuestion.objects.filter(quiz=quiz)
    txtQuestions = TextQuestion.objects.filter(quiz=quiz)
    cbQuestions = CheckboxQuestion.object.filter(quiz=quiz)
    total_questions = len(boolQuestions) + len(mcQuestions) + len(txtQuestions) + len(cbQuestions)


    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'total_questions': total_questions,
        'boolQuestions': boolQuestions,
        'txtQuestions': txtQuestions,
        'mcQuestions': mcQuestions,
        'cbQuestions': cbQuestions
    })
