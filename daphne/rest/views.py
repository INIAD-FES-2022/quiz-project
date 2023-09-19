from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics
from quiz.models import UserScores
from rest.serializers import RankingSerializer


class RankingList(generics.ListAPIView):
    serializer_class = RankingSerializer

    def get_queryset(self):
        queryset = UserScores.objects.all()
        params = self.request.query_params

        userid = params.get('userid', None)
        eventid = params.get('eventid', None)
        if userid is not None:
            try:
                queryset = queryset.filter(user_id__exact=userid)
            except ValidationError:
                pass
        if eventid is not None:
            try:
                queryset = queryset.filter(event_id__exact=eventid)
            except:
                pass
        return queryset
