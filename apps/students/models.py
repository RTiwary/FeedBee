from django.db import models
from apps.teachers.models import Survey, MultipleChoiceQuestion, BooleanQuestion, CheckboxQuestion, TextQuestion, \
    Classroom
from apps.users.models import *


class BooleanAnswer(models.Model):
    question = models.ForeignKey(BooleanQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    answer = models.BooleanField(null=True)


class TextAnswer(models.Model):
    question = models.ForeignKey(TextQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, null=True)


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, null=True)  # store letter to choose


class CheckboxAnswer(models.Model):
    question = models.ForeignKey(CheckboxQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5, null=True, blank=True)
