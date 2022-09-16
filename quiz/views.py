from msilib.schema import ListView
from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from quiz.models import Questions, UserAnswers, Quizzes
import uuid
# Create your views here.

def debugTop(request):
    return HttpResponse("Debug Top!")

def dbgScoring(request, quizUuid):
    quiz = Quizzes.objects.get(id=quizUuid)
    answers = UserAnswers.objects.filter(quiz=quiz).filter(choice=quiz.question.correctChoice)
    context = {
        "quiz": quiz,
        "object_list": answers,
    }
    return render(request, "dbg_scoring.html", context)


class dbgQuestionsList(ListView):
    model = Questions
    fields = "__all__"
    template_name = "dbg_questions_list.html"

class dbgQuestionsCreate(CreateView):
    model = Questions
    template_name = "dbg_create.html"
    fields = "__all__"

class dbgQuizzesList(ListView):
    model = Quizzes
    fields = "__all__"
    template_name = "dbg_quizzes_list.html"

class dbgQuizzesCreate(CreateView):
    model = Quizzes
    template_name = "dbg_create.html"
    fields = "__all__"

class dbgUserAnswersList(ListView):
    model = UserAnswers
    fields = "__all__"
    template_name = "dbg_useranswers_list.html"

class dbgUserAnswersCreate(CreateView):
    model = UserAnswers
    template_name = "dbg_create.html"
    fields = "__all__"
