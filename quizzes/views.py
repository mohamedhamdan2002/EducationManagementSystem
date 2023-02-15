from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import (
    Category, 
    Quiz, 
    Question,
    Answer,
    Submission,
    AnswerItem,
)

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
def categorized_quiz_list_view(request, category_id):
    category = Category.objects.get(category=category_id)
    quiz = category.quizzes.all()
    context = {
        "quizzes": quiz,
    }
    return render(request, 'quizzes/categorized_quiz_list.html', context)

@login_required
def quiz_detail_view(request, category_id, quiz_id):
    if request.POST:
        quiz = Quiz.objects.get(pk=quiz_id) 
        obj = Submission.objects.create(quiz=quiz, user=request.user)
        for q in quiz.questions.all():
            ans = request.POST.get(q.question)
            AnswerItem.objects.create(submission=obj, question=q, answer=Answer.objects.get(answer=ans))
        return redirect(reverse('quizzes:quiz_result', args=(category_id, quiz_id, request.user.get_last_submission().id)))
    quiz = Quiz.objects.get(pk=quiz_id)
    context = {
        "quiz": quiz,
    }
    return render(request, 'quizzes/quiz_detail.html', context)

@login_required
def quiz_result_view(request, category_id, quiz_id, submission_id):
    """
    points = 0
    quiz = Quiz.objects.get(pk=id) 
    obj = Submission.objects.create(quiz=quiz, user=request.user)
    for q in quiz.questions.all():
        ans = request.GET.get(q.question)
        AnswerItem.objects.create(submission=obj, question=q, answer=Answer.objects.get(answer=ans))
        if ans == q.true_answer.answer:
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
    """
    submission = request.user.submissions.get(id=submission_id)
    
    context = {
        'submission': submission,
        'score': submission.get_total_score(),
        'total': len(submission.quiz.questions.all()),
    }

    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def search_view(request):
    return HttpResponseRedirect(reverse('quizzes:categorized_quiz_list', args=(request.GET.get('q'),)))