from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest.views import RankingList, QuizEventsList


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('ranking/', RankingList.as_view()),
    path('events/', QuizEventsList.as_view()),
]
