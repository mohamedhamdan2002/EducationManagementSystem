from django.urls import path

from .views import (
    article_list,
    article_details,
)

app_name = "forums"

urlpatterns = [
    path("", article_list, name="article_list"),
    path("<int:id>/", article_details, name="article_details"),
]
