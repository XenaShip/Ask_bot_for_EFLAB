from django.contrib import admin

from .models import Survey, Question, Answer, Client


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
    list_display = ('survey', 'numb',)
    list_filter = ('survey', 'numb',)
    search_fields = ('survey', 'numb',)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')
