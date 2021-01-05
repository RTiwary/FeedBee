from apps.users.models import *


class Classroom(models.Model):
    name = models.CharField(max_length=20, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="classrooms", null=True)
    students = models.ManyToManyField(Student, related_name="classrooms")


class Survey(models.Model):
    name = models.CharField(max_length=20, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="surveys")
    end_date = models.DateField(null=True)
    frequency = models.CharField(max_length=7, null=True, blank=False)


class BooleanQuestion(models.Model):
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="boolean_questions")
    question_text = models.CharField(max_length=500, null=True)

    question_rank = models.IntegerField(null=True, blank=False)
    question_type = "Boolean"

    display = models.BooleanField(default=True)

    anonymous = models.BooleanField(default=True)


class TextQuestion(models.Model):
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="text_questions")
    question_text = models.CharField(max_length=500, null=True)

    question_rank = models.IntegerField(null=True, blank=False)
    question_type = "Text"

    display = models.BooleanField(default=True)

    anonymous = models.BooleanField(default=True)


class MultipleChoiceQuestion(models.Model):
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="mc_questions")
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=False)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)
    question_type = "MultipleChoice"

    display = models.BooleanField(default=True)

    anonymous = models.BooleanField(default=True)


class CheckboxQuestion(models.Model):
    survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="checkbox_questions")
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=True)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)
    question_type = "Checkbox"

    display = models.BooleanField(default=True)

    anonymous = models.BooleanField(default=True)


# Why didn't we do this?
# class Question(models.Model):
#     survey = models.ForeignKey(Survey, null=True, on_delete=models.CASCADE, related_name="boolean_questions")
#     question_text = models.CharField(max_length=500, null=True)
#
#     question_rank = models.IntegerField(null=True, blank=False)
#
#     display = models.BooleanField(default=True)
#
#     anonymous = models.BooleanField(default=True)
#
#
# class BooleanQuestion(Question):
#     question_type = "Boolean"
#
#
# class TextQuestion(Question):
#     question_type = "Text"
#
#
# class MultipleChoiceQuestion(Question):
#     option_a = models.CharField(max_length=200, null=True, blank=False)
#     option_b = models.CharField(max_length=200, null=True, blank=False)
#     option_c = models.CharField(max_length=200, null=True, blank=True)
#     option_d = models.CharField(max_length=200, null=True, blank=True)
#     option_e = models.CharField(max_length=200, null=True, blank=True)
#
#     question_type = "MultipleChoice"
#
#
# class CheckboxQuestion(Question):
#     option_a = models.CharField(max_length=200, null=True, blank=False)
#     option_b = models.CharField(max_length=200, null=True, blank=True)
#     option_c = models.CharField(max_length=200, null=True, blank=True)
#     option_d = models.CharField(max_length=200, null=True, blank=True)
#     option_e = models.CharField(max_length=200, null=True, blank=True)
#
#     question_type = "Checkbox"
