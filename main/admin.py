from django.contrib import admin

from .models import Survey, Question, Answer, Client, QueText


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('que', 'client', 'ans', 'date')
    list_filter = ('que', 'client', 'ans', 'date')
    search_fields = ('que', 'client', 'ans', 'date')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'acc_tg', 'email', 'phone')
    list_filter = ('name', 'acc_tg', 'email', 'phone')
    search_fields = ('name', 'acc_tg', 'email', 'phone')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('typy_q', 'survey', 'numb',)
    list_filter = ('typy_q', 'survey', 'numb',)
    search_fields = ('typy_q', 'survey', 'numb',)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'description', 'url_survey')
    list_filter = ('slug', 'name', 'description', 'url_survey')
    search_fields = ('slug', 'name', 'description', 'url_survey')


@admin.register(QueText)
class QueText(admin.ModelAdmin):
    list_display = ('que', 'your_text')
    list_filter = ('que', 'your_text')
    search_fields = ('que', 'your_text')