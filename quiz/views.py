from msilib.schema import ListView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic import TemplateView
from quiz.models import Questions, QuizEvents, UserAnswers, Quizzes
from django import forms

import quiz.quiz_functions as qfc
# Create your views here.

class ControlQuizEvents(ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_events.html"


class ControlQuizEventsDetail(SingleObjectMixin, ListView):
    template_name = "control_quiz_events_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=QuizEvents.objects.all())
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.object.quizzes.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_event"] = self.object
        print(context)
        return context
    

class ControlQuizEventsAddQuiz(CreateView):
    model = Quizzes
    fields = ["question"]
    template_name = "control_quiz_events_add_quiz.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields["question"].widget = forms.RadioSelect()
        form.fields["question"].empty_label = None
        form.fields["question"].queryset = Questions.objects.all()
        print(form)
        return form
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.event = QuizEvents.objects.get(pk=self.kwargs["pk"])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse("control_quiz_events_detail", kwargs={"pk": self.kwargs["pk"]})

class ControlQuizHistory(ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_history.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst=[]
        for obj in context["object_list"]:
            lst.append(qfc.get_users_score(obj.id))
        context["event_ranking"] = lst
        return context

class ControlQuizOperate(ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_operate.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst=[]
        for obj in context["object_list"]:
            qs_lst = []
            qz_lst = Quizzes.objects.filter(event=obj.id)
            for qz in qz_lst:
                qs_lst.append(Questions.objects.get(pk=qz.question_id))
            lst.append(qs_lst)
        context["questions"] = lst
        print(context)
        return context


def debugTop(request):
    return HttpResponse("Debug Top!")

def dbgQuizOpen(request, quizUuid):
    quiz = Quizzes.objects.get(id=quizUuid)
    question = quiz.question

    message = {
        "messageType": "quizOpen",
        "sentence": question.sentence,
        "choices": [question.choiceA, question.choiceB, question.choiceC, question.choiceD,],
    }

    print(message)

    qfc.all_user_send_message(message)

    return HttpResponse("Successfully opened quiz.")

def dbgScoring(request, quizUuid):
    quiz = Quizzes.objects.get(id=quizUuid)
    scored_users = qfc.get_scored_users(quizUuid)
    
    qfc.users_add_score(quiz.event.id, scored_users.get("correct"), 20, True)

    message = {
        "messageType": "scoringResult",
        "correctChoice": quiz.question.correctChoice,
        "isCorrect": None,
    }

    message["isCorrect"] = True
    for user in scored_users.get("correct"):
        qfc.user_send_message(user, message)
    
    message["isCorrect"] = False
    for user in scored_users.get("incorrect"):
        qfc.user_send_message(user, message)
    
    context = {
        "quiz": quiz,
        "object_list": scored_users,
    }
    return render(request, "dbg_scoring.html", context)

def dbgSendRanking(request, event_id):
    qfc.update_ranking(event_id)
    users_score = qfc.get_users_score(event_id)

    for user in users_score:
        message = {
            "messageType": "rankDisplay",
            "rank": user.temp_rank,
            "score": user.score,
            "correctNums": user.correctNums,
        }
        qfc.user_send_message(user.user.id, message)

    context = {
        "object_list": users_score,
    }
    
    return render(request, "dbg_sendranking.html", context)


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
