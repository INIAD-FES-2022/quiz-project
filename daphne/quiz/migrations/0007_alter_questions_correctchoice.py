# Generated by Django 4.1.1 on 2022-10-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_userscores_temp_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='correctChoice',
            field=models.CharField(choices=[(None, '正解を選択'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, verbose_name='正解'),
        ),
    ]
