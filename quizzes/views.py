from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from .form import QuizForm,QuestionForm,QuestionFromset,TagFromset,AnswerFormset,AnswerForm
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
    Tformset=TagFromset(request.POST or None) # T ->tag
    formset=QuestionFromset(request.POST or None)
    context={
        'quiz_form':quiz_form,
        'formset':formset,
        'Tformset':Tformset
    }
    if all([quiz_form.is_valid(),formset.is_valid(),Tformset.is_valid()]):
        quiz=quiz_form.save()
        for form in formset:
            try:
                if not form.cleaned_data['DELETE']:
                    qs=Question.objects.get(id=form.cleaned_data['question'].id)
                    quiz.questions.add(qs)
            except:
                continue
        for form in Tformset:
            try:
                if not form.cleaned_data['DELETE']:
                    qs=Tag.objects.get(id=form.cleaned_data['tag'].id)
                    quiz.tags.add(qs)
            except:
                continue
        return redirect(quiz.get_absolute_url())
    return render(request,'staff/update_create.html',context)


@login_required
@admin_only
def admin_update_quiz(request,quiz_id=None):
    quiz_obj=get_object_or_404(Quiz,id=quiz_id)
    quiz_form=QuizForm(request.POST or None,instance=quiz_obj)
    formset=QuestionFromset(request.POST or None,instance=quiz_obj)
    Tformset=TagFromset(request.POST or None,instance=quiz_obj) # T ->tag
    context={
        'quiz': quiz_obj,
        'quiz_form':quiz_form,
        'formset':formset,
        'Tformset':Tformset,
    }
    if all([quiz_form.is_valid(),formset.is_valid(),Tformset.is_valid()]):
        quiz=quiz_form.save()
        for form in formset:
            try:
                q=Question.objects.get(id=form.cleaned_data['question'].id)
                if form.cleaned_data['DELETE']:
                    quiz.questions.remove(q)
                else:
                    qs=quiz.questions.all()
                    if q not in qs:
                        quiz.questions.add(q)
            except:
                continue
        for form in Tformset:
            try:
                q=Tag.objects.get(id=form.cleaned_data['tag'].id)
                if form.cleaned_data['DELETE']:
                    quiz.tags.remove(q)
                else:
                    qs=quiz.tags.all()
                    if q not in qs:
                        quiz.tags.add(q)
            except:
                continue            
        return redirect(quiz.get_absolute_url())
    return render(request,'staff/update_create.html',context)


@login_required
@admin_only
def admin_quiz_detail_view(request,quiz_id=None):
    quiz=get_object_or_404(Quiz,id=quiz_id)
    context={
        "quiz":quiz,
    }
    return render(request,"staff/quiz_detail.html",context)



@login_required
@admin_only
def admin_create_questions(request):
    question_form=QuestionForm(request.POST or None)
    formset=AnswerFormset(request.POST or None)
    context={
        'question_form':question_form,
        'formset':formset,
    }
    if all([question_form.is_valid(),formset.is_valid()]):
        question=question_form.save()
        for form in formset:
            try:
                if not form.cleaned_data['DELETE']:
                    qs=Answer.objects.get(id=form.cleaned_data['answer'].id)
                    question.answers.add(qs)
            except:
                continue
        return redirect(question.get_absolute_url())
    return render(request,'staff/question_update_create.html',context)


@login_required
@admin_only
def admin_update_questions(request,question_id=None):
    question_obj=get_object_or_404(Question,id=question_id)
    question_form=QuestionForm(request.POST or None,instance=question_obj)
    formset=AnswerFormset(request.POST or None,instance=question_obj)
    context={
        'question_form':question_form,
        'formset':formset,
    }
    if all([question_form.is_valid(),formset.is_valid()]):
        question=question_form.save()
        for form in formset:
            try:
                ans=Answer.objects.get(id=form.cleaned_data['answer'].id)
                if form.cleaned_data['DELETE']:
                    question.answers.remove(ans)
                else:
                    answers=question.answers.all()
                    if ans not in answers:
                        question.answers.add(ans)
            except:
                continue
        return redirect(question.get_absolute_url())
    return render(request,'staff/question_update_create.html',context)


@login_required
@admin_only
def admin_questions_list_view(request):
    questions=Question.objects.all()
    context={
        "questions":questions,
    }
    return render(request,"staff/question_list.html",context)

@login_required
@admin_only
def admin_َquestion_detail_view(request,question_id=None):
    question=get_object_or_404(Question,id=question_id)
    context={
        "question":question,
    }
    return render(request,"staff/question_detail.html",context)


@login_required
@admin_only
def admin_create_answer(request):
    form=AnswerForm(request.POST or None)
    context={
        "form":form
    }
    if form.is_valid():
        form.save();
        return redirect('/')
    return render(request,'staff/answer_create.html',context)






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
    return render(request, 'quizzes/quiz_list.html', context)

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
        'total': submission.quiz.questions.all().count(),
    }

    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def search_view(request):
    return HttpResponseRedirect(reverse('quizzes:categorized_quiz_list', args=(request.GET.get('q'),)))
