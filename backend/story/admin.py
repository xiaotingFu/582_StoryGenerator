
# todo/admin.py
    
from django.contrib import admin
from .models import Story # add this
    
class StoryAdmin(admin.ModelAdmin):  # add this
  list_display =('book1', 'book2', 'title', 'url') # add this
        
# Register your models here.
admin.site.register(Story, StoryAdmin) # add this