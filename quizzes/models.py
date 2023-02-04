from django.db import models



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

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
            Category,
            on_delete = models.CASCADE,
            related_name = 'quizzes',
    )
    difficulty = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title