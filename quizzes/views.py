from django.shortcuts import render

from .models import Category

def category_list_view(request):
    q = Category.objects.all()
    context = {
        "categories": q,
    }
    return render(request, 'quizzes/category_list.html', context)