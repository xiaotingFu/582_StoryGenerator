
# todo/views.py

from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import StorySerializer      # add this
from .models import Story                     # add this
        
class TodoView(viewsets.ModelViewSet):       # add this
  serializer_class = StorySerializer          # add this
  queryset = Story.objects.all()              # add this