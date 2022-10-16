from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic import TemplateView
from quiz.models import Questions, QuizEvents, UserAnswers, Quizzes, UserScores
from django import forms

import quiz.quiz_functions as qfc
# Create your views here.

# 管理者認証用Mixin
class SuperuserRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy("admin:login")

    def test_func(self):
        return self.request.user.is_superuser

class ControlQuizTop(SuperuserRequiredMixin, TemplateView):
    template_name = "control_quiz_toppage.html"

class ControlQuizEvents(SuperuserRequiredMixin, ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_events.html"


class ControlQuizEventsDetail(SuperuserRequiredMixin, SingleObjectMixin, ListView):
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
    

class ControlQuizEventsAddQuiz(SuperuserRequiredMixin, CreateView):
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

class ControlQuizHistory(SuperuserRequiredMixin, ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_history.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst=[]
        for obj in context["object_list"]:
            lst.append(qfc.get_users_score(obj.id).order_by("temp_rank"))
        context["event_ranking"] = lst
        print(context)
        return context

class ControlQuizOperate(SuperuserRequiredMixin, ListView):
    model = QuizEvents
    fields = ["id", "name"]
    template_name = "control_quiz_operate.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lst=[]
        for obj in context["object_list"]:
            qz_lst = Quizzes.objects.select_related("question").filter(event=obj.id)
            """
            # Quizzesのpk(出題ごとに一意)で採点も行うためQuizzesオブジェクトで取得。
            for qz in qz_lst:
                qs_lst.append(Questions.objects.get(pk=qz.question_id))
            """
            lst.append(qz_lst)
        context["questions"] = lst
        print(context["questions"])
        return context

class IndexView(ListView):
    model = UserScores
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userScores'] = UserScores.objects.filter(temp_rank__range=(1,10), event=QuizEvents.objects.latest('name'));
        return context


class QuizPlayView(TemplateView):
    template_name = "quiz_play.html"


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
