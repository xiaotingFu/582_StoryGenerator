
# todo/models.py
      
from django.db import models
# Create your models here.

# add Story
class Story(models.Model):
  book1 = models.CharField(max_length=120)
  book2 = models.CharField(max_length=120)
  title = models.CharField(max_length=120)
  url = models.TextField()
      
