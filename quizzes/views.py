from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.forms.models import modelformset_factory,inlineformset_factory

from .form import QuizForm,QuetionForm,TagForm,TagForm
from accounts.decorators import admin_only

from .models import (
    Category, 
    Quiz, 
    Question,
    Tag,
    Answer,
    Submission,
    AnswerItem,
)

@login_required
@admin_only
def admin_create_quiz(request):
    quiz_form=QuizForm(request.POST or None)
    QuetionFromset=inlineformset_factory(Quiz,Quiz.questions.through,exclude=['questions'],extra=0)
    TageFromset=inlineformset_factory(Quiz,Quiz.tags.through,exclude=['tags'],extra=0)
    Tformset=TageFromset(request.POST or None) # T ->tag
    formset=QuetionFromset(request.POST or None)
    context={
        'quiz_form':quiz_form,
        'formset':formset,
        'Tformset':Tformset
    }
    if all([quiz_form.is_valid(),formset.is_valid(),Tformset.is_valid()]):
        quiz=quiz_form.save(commit=False)
        quiz.save()
        for form in formset:
            qs=Question.objects.get(id=form.cleaned_data['question'].id)
            quiz.questions.add(qs)
        for form in Tformset:
            qs=Tag.objects.get(id=form.cleaned_data['tag'].id)
            quiz.tags.add(qs)
        return redirect(quiz.get_absolute_url())
    return render(request,'staff/update-create.html',context)


@login_required
@admin_only
def admin_update_quiz(request,quiz_id=None):
    quiz_obj=get_object_or_404(Quiz,id=quiz_id)
    quiz_form=QuizForm(request.POST or None,instance=quiz_obj)
    QuetionFromset=inlineformset_factory(Quiz,Quiz.questions.through,exclude=['questions'],extra=0)
    formset=QuetionFromset(request.POST or None,instance=quiz_obj)
    TageFromset=inlineformset_factory(Quiz,Quiz.tags.through,exclude=['tags'],extra=0)
    Tformset=TageFromset(request.POST or None,instance=quiz_obj) # T ->tag
    context={
        'quiz_form':quiz_form,
        'formset':formset,
        'Tformset':Tformset,
    }
    if all([quiz_form.is_valid(),formset.is_valid(),Tformset.is_valid()]):
        quiz=quiz_form.save(commit=False)
        quiz.save()
        print(formset.cleaned_data)
        for form in formset:
            q=Question.objects.get(id=form.cleaned_data['question'].id)
            if form.cleaned_data['DELETE']:
                quiz.questions.remove(q)
            else:
                qs=quiz.questions.all()
                if q not in qs:
                    quiz.questions.add(q)
        for form in Tformset:
            q=Tag.objects.get(id=form.cleaned_data['tag'].id)
            if form.cleaned_data['DELETE']:
                quiz.tags.remove(q)
            else:
                qs=quiz.tags.all()
                if q not in qs:
                    quiz.tags.add(q)            
        return redirect(quiz.get_absolute_url())
    return render(request,'staff/update-create.html',context)


@login_required
@admin_only
def admin_quiz_detail_view(request,quiz_id=None):
    quiz=get_object_or_404(Quiz,id=quiz_id)
    context={
        "quiz":quiz,
    }
    return render(request,"staff/quiz-detail.html",context)



# @login_required
# @admin_only
# def admin_create_quiz(request):
#     quiz_form=QuizForm(request.POST or None)
#     QuetionFromset=inlineformset_factory(Quiz,Quiz.questions.through,exclude=['questions'],extra=0)
#     TageFromset=inlineformset_factory(Quiz,Quiz.tags.through,exclude=['tags'],extra=0)
#     Tformset=TageFromset(request.POST or None) # T ->tag
#     formset=QuetionFromset(request.POST or None)
#     context={
#         'quiz_form':quiz_form,
#         'formset':formset,
#         'Tformset':Tformset
#     }
#     if all([quiz_form.is_valid(),formset.is_valid(),Tformset.is_valid()]):
#         quiz=quiz_form.save(commit=False)
#         quiz.save()
#         for form in formset:
#             qs=Question.objects.get(id=form.cleaned_data['question'].id)
#             quiz.questions.add(qs)
#         for form in Tformset:
#             qs=Tag.objects.get(id=form.cleaned_data['tag'].id)
#             quiz.tags.add(qs)
#         return redirect(quiz.get_absolute_url())
#     return render(request,'staff/update-create.html',context)



@login_required
@admin_only
def admin_questions_list_view(request):
    questions=Question.objects.all()
    context={
        "questions":questions,
    }
    return render(request,"staff/question-list.html",context)

  


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
        submission = request.user.get_last_submission(quiz)
        submission.finished = True
        submission.save()
        if submission.ended():
            return render(request, 'quizzes/quiz_result.html', {'error': 'Time is up'})
        for q in quiz.questions.all():
            ans = request.POST.get(q.question)
            AnswerItem.objects.create(submission=submission, question=q, answer=Answer.objects.get(answer=ans))
        return redirect(reverse('quizzes:quiz_result', args=(category_id, quiz_id, request.user.get_last_submission(quiz=quiz).id)))
    quiz = Quiz.objects.get(pk=quiz_id)
    
    submission = None
    try:
        subm = request.user.get_last_submission(quiz)
        if subm.finished or subm.ended():
            submission  = Submission.objects.create(quiz=quiz, user=request.user) 
        else:
            submission = subm
    except:
        submission  = Submission.objects.create(quiz=quiz, user=request.user)
    context = {
        "quiz": quiz,
        "start": submission.start_time,
        "end": submission.end_time(),
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