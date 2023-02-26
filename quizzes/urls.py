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
    admin_update_questions,
    admin_َquestion_detail_view,
    admin_create_answer,
    admin_answers_list_view,
    admin_update_answer,
    admin_update_category,
    admin_create_category,
    admin_category_list_view,
    admin_delete_quiz,
    admin_delete_answer,
    admin_delete_category,
    admin_delete_question,

)

app_name = 'quizzes'

urlpatterns = [
    path('', category_list_view, name='quiz_list'),
    path('categories/',admin_category_list_view,name='category_list'),
    path('categories/create/',admin_create_category,name='create_category'),
    path('categories/<int:category_id>/edit/',admin_update_category,name='edit_category'),
    path('categories/<int:category_id>/delete/',admin_delete_category,name='delete_category'),
    path('questions/',admin_questions_list_view,name='question_list'),
    path('questions/create/',admin_create_questions,name='create_question'),
    path('questions/<int:question_id>/edit/',admin_update_questions,name='edit_question'),
    path('questions/<int:question_id>/delete/',admin_delete_question,name='delete_question'),
    path('qustions/answers/',admin_answers_list_view,name='answer_list'),
    path('questions/answers/create/',admin_create_answer,name='create_answer'),
    path('questions/answers/<int:answer_id>/edit/',admin_update_answer,name='edit_answer'),
    path('questions/answers/<int:answer_id>/delete/',admin_delete_answer,name='delete_answer'),
    path('questions/<int:question_id>/detail/',admin_َquestion_detail_view,name='question_detail'),
    path('create/',admin_create_quiz,name='create_quiz'),
    path('<int:quiz_id>/edit/',admin_update_quiz,name='edit_quiz'),
    path('<int:quiz_id>/detail/',admin_quiz_detail_view,name='quiz_detail'),
    path('<int:quiz_id>/delete/',admin_delete_quiz,name='delete_quiz'),
    path('categories/<slug:category_id>/', categorized_quiz_list_view, name='categorized_quiz_list'),
    path('categories/<slug:category_id>/<int:quiz_id>/', quiz_detail_view, name='quiz_detail'),
    path('categories/<slug:category_id>/<int:quiz_id>/result/<slug:submission_id>/', quiz_result_view, name='quiz_result'),
    path('search/', search_view, name='search'),
]
