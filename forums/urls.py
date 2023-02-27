from django.urls import path

from .views import (
    article_list_view,
    article_detail_view,
)

app_name = "forums"

urlpatterns = [
    path("", article_list_view, name="article_list"),
    path("<int:article_id>/", article_detail_view, name="article_detail"),
]
