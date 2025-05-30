# backend/api/admin.py

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'author', 'date', 'emotion_primary', 'emotion_score', 'true_emotion_label')
    list_filter = ('platform', 'emotion_primary', 'date')
    search_fields = ('content', 'author', 'external_id')
    date_hierarchy = 'date'
    ordering = ('-date',)