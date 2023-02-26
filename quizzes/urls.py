from django.urls import path

from .views import (
    category_list_view, 
    categorized_quiz_list_view,
    quiz_detail_view,
    quiz_result_view,
    search_view,
    admin_create_quiz,
    admin_update_quiz,
    admin_quiz_detail_view,
    admin_questions_list_view,
    admin_create_questions,
    admin_update_question,
    admin_َquestion_detail_view,

)

app_name = 'quizzes'

urlpatterns = [
    path('', category_list_view, name='quiz_list'),
    path('questions/',admin_questions_list_view,name='question_list'),
    path('questions/create/',admin_create_questions,name='create_question'),
    path('questions/<int:question_id>/edit/',admin_update_question,name='edit_question'),
    path('questions/<int:question_id>/detail/',admin_َquestion_detail_view,name='question_detail'),
    path('create/',admin_create_quiz,name='create_quiz'),
    path('<int:quiz_id>/edit/',admin_update_quiz,name='edit_quiz'),
    path('<int:quiz_id>/detail/',admin_quiz_detail_view,name='quiz_detail'),
    path('categories/<slug:category_id>/', categorized_quiz_list_view, name='categorized_quiz_list'),
    path('categories/<slug:category_id>/<int:quiz_id>/', quiz_detail_view, name='quiz_detail'),
    path('categories/<slug:category_id>/<int:quiz_id>/result/<slug:submission_id>/', quiz_result_view, name='quiz_result'),
    path('search/', search_view, name='search'),
]
