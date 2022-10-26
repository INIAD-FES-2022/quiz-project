from django.contrib import admin
from quiz.models import Questions, UserAnswers, Quizzes, UserData, QuizEvents, UserScores

# Register your models here.

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("sentence", "choiceA", "choiceB", "choiceC", "choiceD", "correctChoice")

class QuizEventsAdmin(admin.ModelAdmin):
    list_display = ("name",)

class QuizzesAdmin(admin.ModelAdmin):
    list_display = ("question", "event")
    fields = ("question", "event")

admin.site.register(QuizEvents, QuizEventsAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Quizzes, QuizzesAdmin)