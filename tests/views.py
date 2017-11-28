from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Article


def article(request, id):
    article = get_object_or_404(Article.objects.published(request), id=id)
    return HttpResponse(article.id)
