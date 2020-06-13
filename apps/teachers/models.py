from apps.users.models import *


class Classroom(models.Model):
    name = models.CharField(max_length=100, null=True)
<<<<<<< HEAD
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="classroom")
    students = models.ManyToManyField(Student, related_name="classroom")

=======
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="classrooms", null=True)
    students = models.ManyToManyField(Student, related_name="classrooms")
>>>>>>> master

class Survey(models.Model):
    name = models.CharField(max_length=100, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="surveys")
    unit = models.CharField(max_length=75, null=True)
    school_year = models.CharField(max_length=9, null=True)
    term = models.CharField(max_length=1, null=True)
    completed_students = models.ManyToManyField(Student, related_name="survey")
    creation_date = models.DateTimeField(auto_now_add=True, null=True)


class BooleanQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="boolean_questions")
    question_text = models.CharField(max_length=500, null=True)

<<<<<<< HEAD
=======
    question_rank = models.IntegerField(null=True, blank=False)
>>>>>>> master

class TextQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="text_questions")
    question_text = models.CharField(max_length=500, null=True)

<<<<<<< HEAD
=======
    question_rank = models.IntegerField(null=True, blank=False)
>>>>>>> master

class MultipleChoiceQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="mc_questions")
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=False)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)

<<<<<<< HEAD

=======
>>>>>>> master
class CheckboxQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="checkbox_questions")
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=True)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)
