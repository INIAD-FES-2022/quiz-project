from django.urls import path, include
from . import views

urlpatterns = [
    path("debug/", views.debugTop),
    path("debug/questions/", views.dbgQuestionsList.as_view(), name="questions_list"),
    path("debug/questions/create", views.dbgQuestionsCreate.as_view()),
    path("debug/useranswers/", views.dbgUserAnswersList.as_view(), name="useranswers_list"),
    path("debug/useranswers/create", views.dbgUserAnswersCreate.as_view()),
    path("debug/quizzes/", views.dbgQuizzesList.as_view(), name="quizzes_list"),
    path("debug/quizzes/create", views.dbgQuizzesCreate.as_view()),
    path("debug/scoring/<uuid:quizUuid>", views.dbgScoring),
    path("debug/socket/", views.dbgSocket.as_view()),
    path("debug/sendranking/<int:event_id>", views.dbgSendRanking),
]
