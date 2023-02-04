from django.shortcuts import render

from .models import Category, Quiz, Question

def category_list_view(request):
    categories = Category.objects.all()
    quizzes = Quiz.objects.all()
    context = {
        "categories": categories,
        "quizzes": quizzes,
    }
    return render(request, 'quizzes/quiz_list.html', context)

def categorized_quiz_list_view(request, category):
    category = Category.objects.get(category=category)
    quiz = category.quizzes.all()
    context = {
        "quizzes": quiz,
    }
    return render(request, 'quizzes/categorized_quiz_list.html', context)

def quiz_detail_view(request, category, id):
    quiz = Quiz.objects.get(pk=id)
    context = {
        "quiz": quiz,
    }
    return render(request, 'quizzes/quiz_detail.html', context)

def quiz_result_view(request, category, id):
    points = 0
    quiz = Quiz.objects.get(pk=id)
    for q in quiz.questions.all():
        if request.GET.get(q.question) == q.true_answer.answer:
            points += 1
    context = {
        "result": points,
        "total": len(request.GET),
    }
    return render(request, 'quizzes/quiz_result.html', context)