from django.shortcuts import render
from rest_framework import viewsets
from quiz.models import UserScores
from rest.serializers import RankingSerializer


class RankingViewSet(viewsets.ModelViewSet):
    queryset = UserScores.objects.all()
    serializer_class = RankingSerializer

# Create your views here.
