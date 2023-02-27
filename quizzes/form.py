from django import forms
from django.forms.models import inlineformset_factory
from .models import Quiz,Question,Answer,Tag,Category


QuestionFromset=inlineformset_factory(Quiz,Quiz.questions.through,exclude=['questions'],extra=0)
TagFromset=inlineformset_factory(Quiz,Quiz.tags.through,exclude=['tags'],extra=0)
AnswerFormset=inlineformset_factory(Question,Question.answers.through,exclude=['answers'],extra=0)

class QuizForm(forms.ModelForm):
    class Meta:
        model=Quiz
        fields=[
            'title',
            'category',
            'difficulty',
            'duration',
            'daily_subm_limit',
        ]
class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=[
            'question',
            'true_answer',
            'q_type',
        ]
class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answer
        fields=[
            'answer'
        ]

class TagForm(forms.ModelForm):
    class Meta:
        model=Tag
        fields=[
            'tag'
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=[
            'category'
        ]

