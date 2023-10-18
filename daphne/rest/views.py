from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics
from quiz.models import UserScores, QuizEvents
from rest.serializers import RankingSerializer, QuizEventsSerializer


class RankingList(generics.ListAPIView):
    serializer_class = RankingSerializer

    def get_queryset(self):
        queryset = UserScores.objects.all()
        params = self.request.query_params

        userid = params.get('userid', None)
        eventid = params.get('eventid', None)
        if userid is not None:
            try:
                queryset = queryset.filter(user=userid)
            except ValidationError:
                pass
        if eventid is not None:
            try:
                queryset = queryset.filter(event=eventid)
            except:
                pass
        queryset = queryset.order_by('temp_rank')
        return queryset


class QuizEventsList(generics.ListAPIView):
    serializer_class = QuizEventsSerializer
    
    def get_queryset(self):
        queryset = QuizEvents.objects.filter(is_active=True)
        return queryset
