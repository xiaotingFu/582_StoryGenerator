# story/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from story import views

urlpatterns = [
    path('story/', views.SnippetList.as_view()),
    path('story/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)