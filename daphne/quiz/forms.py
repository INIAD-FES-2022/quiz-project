from django import forms
from quiz.models import Questions


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSVファイル')


class AssociateForm(forms.Form):
    question_choices = forms.ModelMultipleChoiceField(
        queryset=Questions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="QuizEventと選択した問題を結びつけます"
    )
