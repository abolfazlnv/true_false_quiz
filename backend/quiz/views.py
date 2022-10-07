from django.contrib import messages
from django.urls import reverse
from quiz.models import Quiz, Question, UserAnswer
from quiz.forms import AnswerForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View, ListView, FormView
from django.http import HttpResponseRedirect

class QuizList(LoginRequiredMixin, ListView):
    model = Quiz
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_answer = UserAnswer.objects.filter(user=user)
        if user_answer:
            context['answered'] = True
        else:
            context['answered'] = False
        return context


class QuizDetail(LoginRequiredMixin, DetailView):
    model = Quiz
    context_object_name = 'quiz'
    queryset = Quiz.objects.all()

    def first_question(self):
        return self.object.question_set.all()[0]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_answer = UserAnswer.objects.filter(user=user)
        if user_answer:
            context['answered'] = True
        else:
            context['answered'] = False
        return context


class QuestionList(LoginRequiredMixin, ListView):
    model = Question

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Question.objects.filter(quiz=pk)

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['quiz'] = self.kwargs.get('pk')
        return context


class AnswerFormView(LoginRequiredMixin,FormView):
    template_name = 'quiz/answer_form.html'
    form_class = AnswerForm
    success_url = 'list/'
    
    def get_form_kwargs(self):
        kwargs = super(AnswerFormView, self).get_form_kwargs()
        quiz=self.kwargs['number']
        questions = Question.objects.filter(quiz = quiz).count()
        kwargs['count'] = questions
        kwargs['quiz'] = quiz
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AnswerFormView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=self.kwargs['number'])
        context['quiz'] = self.kwargs['number']
        return context

    def form_valid(self, form):
        quiz = form.cleaned_data["question"]
        user = self.request.user
        question = Question.objects.filter(quiz=quiz)
        user_answer = UserAnswer.objects.filter(user=user)

        print(f"here {user_answer}")

        if user_answer:
            messages.error(self.request, 'شما در این انتخابات شرکت کرده اید.')
            return redirect(reverse('quiz_list'))

        i = 1
        field_name = 'answer_%s' % (i,)
        while form.cleaned_data.get(field_name):
            answer = form.cleaned_data[field_name]
            UserAnswer.objects.create(question=question[i-1], user=user, answer=answer)
            i += 1
            field_name = 'answer_%s' % (i,)
        return super().form_valid(form)


class QuestionDetail(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    queryset = Question.objects.all()

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = AnswerForm(initial={'question': self.object})
        return context


class LogoutUser(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_active:
            request.user.is_active = False
            logout(request)
            messages.success(request, 'با موفقیت خارج شدید')
        return redirect(reverse('login'))
