from django.contrib import admin
from quiz.models import Quiz, Question, UserAnswer


class QuestionInline(admin.TabularInline):
    model = Question


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(UserAnswer)

