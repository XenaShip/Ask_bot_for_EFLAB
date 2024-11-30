from tkinter.constants import CASCADE

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Survey(models.Model):
    slug = models.SlugField(max_length=255, unique=True, verbose_name='slug')
    name = models.CharField(max_length=50, verbose_name='название опроса')
    description = models.TextField(verbose_name='описание опроса')
    url_survey = models.URLField(verbose_name='ссылка на опрос')
    active = models.BooleanField(verbose_name='активность опроса')
    counting = models.IntegerField(verbose_name='кол-во вопросов в опросе', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return self.name

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'


class Question(models.Model):
    yes_or_no = 'yes_or_no'
    one_of_some = 'one_of_some'
    your_text = 'your_text'

    TYPE_CHOICE = (
        (yes_or_no, 'да или нет'),
        (one_of_some, 'один из'),
        (your_text, 'ваш текст'),
    )
    typy_q = models.CharField(max_length=25, choices=TYPE_CHOICE, verbose_name='тип вопроса')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='опрос')
    numb = models.IntegerField(verbose_name='номер вопроса')
    count_marks = models.IntegerField(verbose_name='количество кнопок')

    def __str__(self):
        return f'{self.survey}, {self.numb}'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class QueText(models.Model):
    que = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='ссылаемый вопрос')
    your_text = models.TextField(verbose_name='текст ответа')

    def __str__(self):
        return self.your_text

    class Meta:
        verbose_name = 'текст вопроса'
        verbose_name_plural = 'текст вопросов'


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    que = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='вопрос')
    ans = models.TextField(verbose_name='ответ')
    date = models.DateTimeField(auto_now_add=True, verbose_name='время ответа')

    def __str__(self):
        return f'{self.client.name}'

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'