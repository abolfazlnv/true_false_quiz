from urllib import request
from django import forms
from quiz.models import Question, UserAnswer


class AnswerForm(forms.Form):
    # answer = forms.ChoiceField(widget=forms.RadioSelect, choices=((True, ''), (False, 'False')))
    question = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, count, quiz, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        questions = Question.objects.filter(quiz=quiz)
        for i in range(1, count+1):
            self.fields["answer_%d" % i] = forms.ChoiceField(widget=forms.RadioSelect, choices=((True, 'موافقم'), (False, 'مخالفم')), label=f"{questions[i-1]}")

    def clean(self):
        answers = set()
        i = 1
        field_name = 'answer_%s' % (i,)
        while self.cleaned_data.get(field_name):
            answer = self.cleaned_data[field_name]
            answers.add(answer)
            i += 1
            field_name = 'answer_%s' % (i,)
        self.cleaned_data["answers"] = answers

    def save(self):
        quiz = self.cleaned_data["question"]
        user = self.request.user
        question = Question.objects.filter(quiz=quiz)

        i = 1
        field_name = 'answer_%s' % (i,)
        while self.cleaned_data.get(field_name):
            answer = self.cleaned_data[field_name]
            print(question[i])
            print(user)
            print(f"answer here : {answer}")
            UserAnswer.objects.create(question=question[i], user=user, answer=answer)
            i += 1
            field_name = 'answer_%s' % (i,)
