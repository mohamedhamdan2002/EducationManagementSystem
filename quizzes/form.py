from django import forms

from .models import Quiz,Question,Answer,Tag,Category


class QuizForm(forms.ModelForm):
    class Meta:
        model=Quiz
        fields=[
            'title',
            'category',
            'difficulty',
            'duration',
        ]
class QuetionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=[
            'question',
            'answers',
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

