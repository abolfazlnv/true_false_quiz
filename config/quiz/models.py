from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=50, default="")
    content = models.TextField()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    statement = models.CharField(max_length=200)

    class Meta:
        verbose_name = "True/false question"
        verbose_name_plural = "True/false questions"

    def __str__(self):
        return self.statement


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()

    class Meta:
        verbose_name = "User answer"
        verbose_name_plural = "User answers"

    def __str__(self):
        return "{}: {}: {}".format(self.user, self.question, self.answer)

