from django.shortcuts import render
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "forums/article_list.html", context)


def article_details(request, id):
    article = Article.objects.get(id=id)
    context = {"article": article}
    return render(request, "forums/article_detail.html", context)
