from tkinter.constants import CASCADE

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Survey(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='slug')
    name = models.CharField(max_length=50, verbose_name='название опроса')
    description = models.TextField(verbose_name='описание опроса')
    active = models.BooleanField(verbose_name='активность опроса')
    counting = models.IntegerField(verbose_name='кол-во вопросов в опросе', **NULLABLE)
    hello_text = models.TextField(verbose_name='приветственный текст', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return self.name

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='опрос')
    numb = models.IntegerField(verbose_name='номер вопроса')
    que_text = models.TextField(verbose_name='текст вопроса', **NULLABLE)

    def __str__(self):
        return f'{self.survey}, {self.numb}'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='фио')
    acc_tg = models.CharField(max_length=100, verbose_name='ТГ аккаунт')
    email = models.EmailField(verbose_name='почта')
    phone = models.CharField(max_length=25, verbose_name='номер телефона')
    tg_id = models.BigIntegerField(unique=True, **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Answer(models.Model):
    client_tg_acc = models.CharField(max_length=100, verbose_name='ТГ аккаунт')
    que = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='вопрос')
    ans = models.TextField(verbose_name='ответ')
    date = models.DateTimeField(auto_now_add=True, verbose_name='время ответа')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='id клиента', **NULLABLE)

    def __str__(self):
        return f'{self.client_tg_acc}'


    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'