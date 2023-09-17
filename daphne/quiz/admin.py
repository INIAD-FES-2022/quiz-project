import csv
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.shortcuts import render
from quiz.forms import CSVUploadForm
from quiz.models import Questions, UserAnswers, Quizzes, UserData, QuizEvents, UserScores

# Register your models here.

class QuestionsAdmin(admin.ModelAdmin):
    change_list_template = "admin/question_changelist.html"
    actions = ['upload_csv']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload-csv/', self.upload_csv, name='upload _csv'),
        ]
        return my_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                csv_data = csv_file.read().decode('utf-8')
                reader = csv.DictReader(csv_data.splitlines())
                for row in reader:
                    Questions.objects.create(
                        sentence=row['sentence'],
                        choiceA=row['choiceA'],
                        choiceB=row['choiceB'],
                        choiceC=row['choiceC'],
                        choiceD=row['choiceD'],
                        correctChoice=row['correctChoice'],
                    )
                self.message_user(request, 'CSVをインポートしました。')
                return HttpResponseRedirect(reverse('admin:quiz_questions_changelist'))
        else:
            form = CSVUploadForm()
        return render(request, 'admin/upload_csv.html', {'form': form})

    upload_csv.short_description = 'CSVをアップロード'

    list_display = ("sentence", "choiceA", "choiceB", "choiceC", "choiceD", "correctChoice")

class QuizEventsAdmin(admin.ModelAdmin):
    list_display = ("name",)

class QuizzesAdmin(admin.ModelAdmin):
    list_display = ("question", "event")
    fields = ("question", "event")

admin.site.register(QuizEvents, QuizEventsAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Quizzes, QuizzesAdmin)
