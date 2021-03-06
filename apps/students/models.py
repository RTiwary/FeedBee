from django.db import models
from apps.teachers.models import Survey, MultipleChoiceQuestion, BooleanQuestion, CheckboxQuestion, TextQuestion, \
    Classroom
from apps.users.models import *


class BooleanAnswer(models.Model):
    question = models.ForeignKey(BooleanQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    answer = models.BooleanField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class TextAnswer(models.Model):
    question = models.ForeignKey(TextQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=500, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(MultipleChoiceQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=1, null=True)  # store letter to choose
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class CheckboxAnswer(models.Model):
    question = models.ForeignKey(CheckboxQuestion, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=5, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
