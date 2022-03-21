from django.contrib import admin
from polls.models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)