from django.db import models
from apps.teachers.models import Survey, MultipleChoiceQuestion, BooleanQuestion, CheckboxQuestion, TextQuestion, \
    Classroom
from apps.users.models import *


class BooleanAnswer(models.Model):
    question = models.ForeignKey(BooleanQuestion, on_delete=models.CASCADE)
    answer = models.BooleanField()


class TextAnswer(models.Model):
    question = models.ForeignKey(TextQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, null=True)


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, null=True)  # store letter to choose


class CheckboxAnswer(models.Model):
    question = models.ForeignKey(CheckboxQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5, null=True, blank=True)
