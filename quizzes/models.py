from math import ceil
import uuid

from django.utils import timezone as tz
from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from datetime import date


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Answer(models.Model):
    answer = models.TextField()

    def __str__(self):
        return self.answer

class Question(models.Model):
    question = models.TextField()
    answers = models.ManyToManyField(Answer)
    true_answer = models.ForeignKey(
            Answer,
            on_delete = models.CASCADE,
            related_name = 'true_for',
    )
    q_type = models.CharField(max_length=50) # denote something like contain matrices or not

    def __str__(self):
        return self.question
    
    def get_absolute_url(self):
        return reverse("quizzes:question_detail",kwargs={'question_id':self.id})

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
            Category,
            on_delete = models.CASCADE,
            related_name = 'quizzes',
    )
    difficulty = models.CharField(max_length=100)
    duration = models.DurationField()
    tags = models.ManyToManyField(Tag)
    questions = models.ManyToManyField(Question)
    daily_subm_limit = models.IntegerField(default=2)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('quizzes:quiz_detail',kwargs={'quiz_id':self.id})

    def score_to_pass(self):
        return ceil((len(self.quiz.questions.all()) * 70.0) / 100.0)

    def daily_subm_limit_exceeded(self, user):
        return self.submissions.filter(user=user, start_time__date=date.today()).count() >= self.daily_subm_limit

class Submission(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    start_time = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.user)} | {str(self.quiz)} | {self.start_time}'

    def get_total_score(self):
        score = 0
        for a in self.items.all():
            if a.question.true_answer == a.answer:
                score += 1
        return score

    def passed(self):
        scored = self.get_total_score()
        return scored >= self.quiz.score_to_pass()

    def end_time(self):
        return self.start_time + self.quiz.duration

    def ended(self):
        return tz.now() > self.end_time()



class AnswerItem(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='items',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{str(self.question)} : {str(self.answer)}'
