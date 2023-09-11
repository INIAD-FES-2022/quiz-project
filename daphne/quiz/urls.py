from django.urls import path, include
from . import views

urlpatterns = [
    path("control/", views.ControlQuizTop.as_view(), name="control_quiz_top"),
    path("control/events", views.ControlQuizEvents.as_view(), name="control_quiz_events"),
    path("control/<int:pk>", views.ControlQuizEventsDetail.as_view(), name="control_quiz_events_detail"),
    path("control/<int:pk>/add_quiz", views.ControlQuizEventsAddQuiz.as_view(), name="control_quiz_events_add_quiz"),
    path("control/history", views.ControlQuizHistory.as_view(), name="control_quiz_history"),
    path("control/operate", views.ControlQuizOperate.as_view(), name="control_quiz_operate"),
    path("", views.IndexView.as_view(), name="index"),
    path("quiz_play", views.QuizPlayView.as_view(), name="join"),
#    path("debug/", views.debugTop),
#    path("debug/questions/", views.dbgQuestionsList.as_view(), name="questions_list"),
#    path("debug/questions/create", views.dbgQuestionsCreate.as_view()),
#    path("debug/useranswers/", views.dbgUserAnswersList.as_view(), name="useranswers_list"),
#    path("debug/useranswers/create", views.dbgUserAnswersCreate.as_view()),
#    path("debug/quizzes/", views.dbgQuizzesList.as_view(), name="quizzes_list"),
#    path("debug/quizzes/create", views.dbgQuizzesCreate.as_view()),
#    path("debug/quizzes/<uuid:quizUuid>/open", views.dbgQuizOpen),
#    path("debug/socket/", views.dbgSocket.as_view()),
]