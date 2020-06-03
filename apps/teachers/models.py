from django.db import models
from apps.users.models import *

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=100, null=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name="teacher")
    students = models.ManyToManyField(Student, related_name="students")

class Survey(models.Model):
    name = models.CharField(max_length=100, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    unit = models.CharField(max_length=75, null=True)
    school_year = models.CharField(max_length=9, null=True)
    term = models.CharField(max_length=1, null=True)

class BooleanQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, null=True)
    question_rank = models.IntegerField(null=True, blank=False)

    recurring = models.BooleanField(null=True)

class TextQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, null=True)
    question_rank = models.IntegerField(null=True, blank=False)

    recurring = models.BooleanField(null=True)

class MultipleChoiceQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=False)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)

    recurring = models.BooleanField(null=True)

class CheckboxQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, null=True)

    option_a = models.CharField(max_length=200, null=True, blank=False)
    option_b = models.CharField(max_length=200, null=True, blank=True)
    option_c = models.CharField(max_length=200, null=True, blank=True)
    option_d = models.CharField(max_length=200, null=True, blank=True)
    option_e = models.CharField(max_length=200, null=True, blank=True)

    question_rank = models.IntegerField(null=True, blank=False)

    recurring = models.BooleanField(null=True)
