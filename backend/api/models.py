# NLP_Emotions_Tracker/backend/api/models.py

from django.db import models
# from django.contrib.postgres.fields import JSONField # If you use PostgreSQL and an older Django version
# If using Django 3.1+ and any database, models.JSONField is preferred:
from django.db.models import JSONField # If you don't have it, you might need to install psycopg2 or django-jsonfield

class Post(models.Model):
    external_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    content = models.TextField()
    platform = models.CharField(max_length=50) # e.g., 'twitter', 'instagram', 'facebook', 'Test_Data'
    author = models.CharField(max_length=100, default='anonymous')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    emotion_primary = models.CharField(max_length=50) # Primary emotion predicted
    emotion_score = models.FloatField() # Confidence score for primary emotion
    secondary_emotions_json = JSONField(default=dict) # Stores all emotion scores as JSON

    # Add this field for the true emotion label from your dataset
    true_emotion_label = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-date'] # Order posts by date, newest first

    def __str__(self):
        return f"{self.platform} - {self.author}: {self.content[:50]}..."
