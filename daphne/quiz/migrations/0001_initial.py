# Generated by Django 4.1.1 on 2022-09-14 15:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sentence', models.CharField(max_length=150, verbose_name='問題')),
                ('choiceA', models.CharField(max_length=50, verbose_name='選択肢A')),
                ('choiceB', models.CharField(max_length=50, verbose_name='選択肢B')),
                ('choiceC', models.CharField(max_length=50, verbose_name='選択肢C')),
                ('choiceD', models.CharField(max_length=50, verbose_name='選択肢D')),
                ('correctChoice', models.CharField(choices=[(None, '正解を選択'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('startTime', models.DateTimeField(auto_now_add=True, verbose_name='解答開始時刻')),
                ('endTime', models.DateTimeField(null=True, verbose_name='解答終了時刻')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='quiz.questions')),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0, verbose_name='得点')),
                ('correctNums', models.IntegerField(default=0, verbose_name='正解数')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='quiz.quizzes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='quiz.userdata')),
            ],
        ),
    ]
