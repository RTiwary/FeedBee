from django.contrib import admin
from .models import BooleanAnswer, MultipleChoiceAnswer, CheckboxAnswer, TextAnswer

# Register your models here.
class BooleanAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "student", "answer", "timestamp")


class TextAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "student", "answer", "timestamp")


class MultipleChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "student", "answer", "timestamp")


class CheckboxAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "student", "answer", "timestamp")


admin.site.register(BooleanAnswer, BooleanAnswerAdmin)
admin.site.register(TextAnswer, TextAnswerAdmin)
admin.site.register(MultipleChoiceAnswer, MultipleChoiceAnswerAdmin)
admin.site.register(CheckboxAnswer, CheckboxAnswerAdmin)
