from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    timezone = models.CharField(default='US/Eastern', max_length=50)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="student_profile")

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="teacher_profile")