# Generated by Django 5.1.3 on 2024-11-29 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='фио')),
                ('acc_tg', models.CharField(max_length=100, verbose_name='ТГ аккаунт')),
                ('email', models.EmailField(max_length=254, verbose_name='почта')),
                ('phone', models.CharField(max_length=25, verbose_name='номер телефона')),
                ('tg_id', models.BigIntegerField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typy_q', models.CharField(choices=[('yes_or_no', 'да или нет'), ('one_of_some', 'один из'), ('your_text', 'ваш текст')], max_length=25, verbose_name='тип вопроса')),
                ('numb', models.IntegerField(verbose_name='номер вопроса')),
                ('count_marks', models.IntegerField(verbose_name='количество кнопок')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=50, verbose_name='название опроса')),
                ('description', models.TextField(verbose_name='описание опроса')),
                ('url_survey', models.URLField(verbose_name='ссылка на опрос')),
                ('active', models.BooleanField(verbose_name='активность опроса')),
                ('counting', models.IntegerField(blank=True, null=True, verbose_name='кол-во вопросов в опросе')),
            ],
            options={
                'verbose_name': 'опрос',
                'verbose_name_plural': 'опросы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.TextField(verbose_name='ответ')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='время ответа')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.client', verbose_name='клиент')),
                ('que', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.question', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='QueText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_text', models.TextField(verbose_name='текст ответа')),
                ('que', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.question', verbose_name='ссылаемый вопрос')),
            ],
            options={
                'verbose_name': 'текст вопроса',
                'verbose_name_plural': 'текст вопросов',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.survey', verbose_name='опрос'),
        ),
    ]
