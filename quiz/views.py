from msilib.schema import ListView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
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
    success_url = reverse_lazy("questions_list")

class dbgQuizzesList(ListView):
    model = Quizzes
    fields = "__all__"
    template_name = "dbg_quizzes_list.html"

class dbgQuizzesCreate(CreateView):
    model = Quizzes
    template_name = "dbg_create.html"
    fields = ["question", "event"]
    success_url = reverse_lazy("quizzes_list")

class dbgUserAnswersList(ListView):
    model = UserAnswers
    fields = "__all__"
    template_name = "dbg_useranswers_list.html"

class dbgUserAnswersCreate(CreateView):
    model = UserAnswers
    template_name = "dbg_create.html"
    fields = "__all__"
    success_url = reverse_lazy("useranswers_list")

class dbgSocket(TemplateView):
    template_name = "dbg_socket.html"