from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest.views import RankingViewSet


router = DefaultRouter()
router.register('ranking', RankingViewSet, 'ranking')

urlpatterns = [
    path('', include(router.urls)),
]
