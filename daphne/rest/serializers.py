from rest_framework import serializers
from quiz.models import UserScores


class RankingSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = UserScores
        fields = ("nickname", "score", "temp_rank")

    def get_nickname(self, obj):
        return obj.user.nickname
