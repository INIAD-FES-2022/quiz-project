from django.urls import path, include
from . import views

urlpatterns = [
    path("debug/", views.debugTop),
    path("debug/questions/", views.dbgQuestionsList.as_view()),
    path("debug/questions/create", views.dbgQuestionsCreate.as_view()),
    path("debug/useranswers/", views.dbgUserAnswersList.as_view()),
    path("debug/useranswers/create", views.dbgUserAnswersCreate.as_view()),
    path("debug/quizzes/", views.dbgQuizzesList.as_view()),
    path("debug/quizzes/create", views.dbgQuizzesCreate.as_view()),
    path("debug/scoring/<uuid:quizUuid>", views.dbgScoring),
    path("debug/socket/", views.dbgSocket.as_view()),
]
