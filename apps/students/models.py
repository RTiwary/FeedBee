from django.db import models
from apps.teachers.models import Survey, MultipleChoiceQuestion, BooleanQuestion, CheckboxQuestion, TextQuestion, Classroom
from apps.users.models import *

# Create your models here.
class BooleanAnswer(models.Model):
    question = models.OneToOneField(BooleanQuestion, on_delete=models.CASCADE)
    answer = models.BooleanField(null=True)

class TextAnswer(models.Model):
    question = models.OneToOneField(TextQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, null=True)

class MultipleChoiceAnswer(models.Model):
    question = models.OneToOneField(MultipleChoiceQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, null=True)  # store letter to choose

class CheckboxAnswer(models.Model):
    question = models.OneToOneField(CheckboxQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=5, null=True, blank=True)