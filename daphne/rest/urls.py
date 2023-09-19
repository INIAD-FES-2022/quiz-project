from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest.views import RankingList


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('ranking/', RankingList.as_view()),
]
