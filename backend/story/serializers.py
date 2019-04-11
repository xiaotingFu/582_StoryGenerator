
# todo/serializers.py

from rest_framework import serializers
from .models import Story
      
class StorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Story
    fields = ('book1', 'book2', 'title', 'url')