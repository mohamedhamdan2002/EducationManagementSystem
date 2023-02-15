from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, Quiz, Question, Score

@login_required
def category_list_view(request):
    categories = Category.objects.all()
    quizzes = Quiz.objects.all()
    context = {
        "categories": categories,
        "quizzes": quizzes,
    }
    return render(request, 'quizzes/quiz_list.html', context)

@login_required
def categorized_quiz_list_view(request, category):
    category = Category.objects.get(category=category)
    quiz = category.quizzes.all()
    context = {
        "quizzes": quiz,
    }
    return render(request, 'quizzes/categorized_quiz_list.html', context)

@login_required
def quiz_detail_view(request, category, id):
    quiz = Quiz.objects.get(pk=id)
    context = {
        "quiz": quiz,
    }
    return render(request, 'quizzes/quiz_detail.html', context)

@login_required
def quiz_result_view(request, category, id):
    points = 0
    quiz = Quiz.objects.get(pk=id) 
    for q in quiz.questions.all():
        if request.GET.get(q.question) == q.true_answer.answer:
            points += 1
    Score.objects.create(quiz=quiz, user=request.user, score=points)
    context = {
        "answers": zip(
            [q.question for q in quiz.questions.all()], 
            [request.GET.get(q.question) for q in quiz.questions.all()],
            [q.true_answer.answer for q in quiz.questions.all()]),
        "result": points,
        "total": len(request.GET),
    }
    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def search_view(request):
    return HttpResponseRedirect(reverse('quizzes:categorized_quiz_list', args=(request.GET.get('q'),)))