from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Article

@login_required
def article_list(request):
    articles = Article.objects.all()
    context = {
        "articles": articles,
    }
    return render(request, "forums/article_list.html", context)

@login_required
def article_details(request, article_id):
    article = Article.objects.get(id=id)
    context = {
        "article": article
    }
    return render(request, "forums/article_detail.html", context)
