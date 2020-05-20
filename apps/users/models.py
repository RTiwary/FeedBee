from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="student_profile")

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="teacher_profile")


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print('****', created)
#     if instance.is_teacher:
#         Teacher.objects.get_or_create(user=instance)
#     else:
#         Student.objects.get_or_create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print('_-----')
#     if instance.is_teacher:
#         instance.intern_profile.save()
#     else:
#         HRProfile.objects.get_or_create(user=instance)