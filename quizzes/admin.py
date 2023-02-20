from django.contrib import admin

from .models import (
    Category,
    Tag,
    Answer,
    Question,
    Quiz,
    Submission,
    AnswerItem,
)

class TagInline(admin.TabularInline):
    model=Quiz.tags.through
    extra=0

class AnswerInline(admin.TabularInline):
    model=Question.answers.through
    extra=0
class QuestionInline(admin.TabularInline):
    model=Quiz.questions.through
    extra=0
    inlines=[AnswerInline]

@admin.register(Question) 
class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]
    exclude=['answers']
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines=[QuestionInline,TagInline]
    exclude=['questions','tags']
    list_display=['title','category','difficulty','duration']
    readonly_fields=['score_to_pass']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Submission)
admin.site.register(AnswerItem)