from django.contrib import admin

from .models import (
    Category,
    Tag,
    Answer,
    Question,
    Quiz,
    Score,  
)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Score)