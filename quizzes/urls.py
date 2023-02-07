from django.urls import path

from .views import (
    category_list_view, 
    categorized_quiz_list_view,
    quiz_detail_view,
    quiz_result_view,
    search_view,
)

app_name = 'quizzes'

urlpatterns = [
    path('', category_list_view, name='quiz_list'),
    path('categories/<slug:category>/', categorized_quiz_list_view, name='categorized_quiz_list'),
    path('categories/<slug:category>/<int:id>/', quiz_detail_view, name='quiz_detail'),
    path('categories/<slug:category>/<int:id>/result/', quiz_result_view, name='quiz_result'),
    path('search/', search_view, name='search'),
]