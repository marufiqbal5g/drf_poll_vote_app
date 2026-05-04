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

]