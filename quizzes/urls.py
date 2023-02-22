from django.urls import path

from .views import (
    category_list_view, 
    categorized_quiz_list_view,
    quiz_detail_view,
    quiz_result_view,
    search_view,
    create_new_quiz
)

app_name = 'quizzes'

urlpatterns = [
    path('', category_list_view, name='quiz_list'),
    path('add-quize',create_new_quiz,name='create'),
    path('categories/<slug:category_id>/', categorized_quiz_list_view, name='categorized_quiz_list'),
    path('categories/<slug:category_id>/<int:quiz_id>/', quiz_detail_view, name='quiz_detail'),
    path('categories/<slug:category_id>/<int:quiz_id>/result/<slug:submission_id>/', quiz_result_view, name='quiz_result'),
    path('search/', search_view, name='search'),
]