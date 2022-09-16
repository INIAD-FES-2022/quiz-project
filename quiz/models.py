from django.db import models
import uuid


# クイズ用のユーザデータを保持。
class UserData(models.Model):
    id = models.UUIDField(primary_key=True)
    score = models.IntegerField(default=0, verbose_name="得点")
    correctNums = models.IntegerField(default=0, verbose_name="正解数")


# 開催回を保持。
class QuizEvents(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称")


# クイズの問題を保持する。
class Questions(models.Model):
    ANSWER_CHOICES = [
        (None, "正解を選択"),
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sentence = models.CharField(max_length=150, verbose_name="問題")
    choiceA = models.CharField(max_length=50, verbose_name="選択肢A")
    choiceB = models.CharField(max_length=50, verbose_name="選択肢B")
    choiceC = models.CharField(max_length=50, verbose_name="選択肢C")
    choiceD = models.CharField(max_length=50, verbose_name="選択肢D")
    correctChoice = models.CharField(max_length=1,choices=ANSWER_CHOICES)


# 出題したクイズの履歴を保持する。
class Quizzes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Questions, on_delete=models.PROTECT, related_name="+")
    event = models.ForeignKey(QuizEvents, on_delete=models.PROTECT, related_name="quizzes")
    startTime = models.DateTimeField(auto_now_add=True, verbose_name="解答開始時刻")
    endTime = models.DateTimeField(null=True, verbose_name="解答終了時刻")


# ユーザの解答を保持。
class UserAnswers(models.Model):
    CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    ]
    quiz = models.ForeignKey(Quizzes, on_delete=models.PROTECT, related_name="answers")
    user = models.ForeignKey(UserData, on_delete=models.PROTECT, related_name="+")
    choice = models.CharField(max_length=1, choices=CHOICES)
