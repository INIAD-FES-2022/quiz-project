# Generated by Django 4.1.1 on 2022-09-16 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
        ),
        migrations.AddField(
            model_name='quizzes',
            name='event',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.PROTECT, related_name='quizzes', to='quiz.quizevents'),
            preserve_default=False,
        ),
    ]
