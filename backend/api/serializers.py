# api/serializers.py

from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # Ensure these field names match your Post model exactly
        fields = [
            'id',
            'external_id',
            'content',
            'author',
            'date',  # Use 'date' instead of 'created_at' and 'updated_at'
            'platform',
            'emotion_primary',
            'emotion_score',
            'likes',
            'secondary_emotions_json',
            'true_emotion_label', # Include this field if you want to expose it
        ]