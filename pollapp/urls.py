from django.urls import path
from . import views

app_name = 'pollapp'

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('create/', views.create, name='create'),
    path('<int:question_id>/results/', views.results, name='results'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('<int:question_id>/delete/', views.delete_question, name='delete_question'),

    path('choice/<int:choice_id>/edit/', views.edit_choice, name='edit_choice'),
    path('choice/<int:choice_id>/delete/', views.delete_choice, name='delete_choice'),

    path('<int:question_id>/add-choice/', views.add_choice, name='add_choice'),

    # API URLs
    path('api/questions/', views.api_questions, name='api_questions'),
    path('api/questions/<int:question_id>/', views.api_question_detail, name='api_question_detail'),
    path('api/questions/create/', views.api_create_question, name='api_create_question'),
    path('api/questions/<int:question_id>/vote/', views.api_vote, name='api_vote'),
    path('api/register/', views.api_register, name='api_register'),
]