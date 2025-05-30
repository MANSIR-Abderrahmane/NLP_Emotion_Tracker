from rest_framework import views
from rest_framework.response import Response
from django.db.models import Count, Avg, F # Import F for database field references
from django.db.models.functions import TruncMonth, TruncDay
from .models import Post
from .serializers import PostSerializer
from collections import defaultdict, OrderedDict
import json

from rest_framework import generics

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EmotionDistributionAPIView(views.APIView):
    """
    API endpoint to get the distribution of primary emotions.
    """
    def get(self, request, *args, **kwargs):
        emotion_counts = Post.objects.values('emotion_primary').annotate(count=Count('emotion_primary'))
        total_posts = Post.objects.count()
        
        distribution = []
        emotion_colors = {
            'Joy': '#4FD1C5',
            'Sadness': '#8884D8',
            'Anger': '#F56565',
            'Surprise': '#ED8936',
            'Fear': '#9F7AEA',
            'Love': '#FF69B4',
            'Error': '#A0AEC0',
            'Neutral': '#90CDF4',
            'Disgust': '#48BB78'
        }

        for item in emotion_counts:
            emotion_name = item['emotion_primary'].capitalize()
            distribution.append({
                'name': emotion_name,
                'value': item['count'],
                'percentage': (item['count'] / total_posts) * 100 if total_posts > 0 else 0,
                'color': emotion_colors.get(emotion_name, '#CCCCCC')
            })
        
        return Response(distribution)

class EmotionTrendAPIView(views.APIView):
    """
    API endpoint to get emotion trends over time, aggregated by month.
    """
    def get(self, request, *args, **kwargs):
        # Annotate posts with their month and year
        # Use F() to reference the model field in TruncMonth
        monthly_posts = Post.objects.annotate(
            month=TruncMonth('date')
        ).values('month', 'emotion_primary').annotate(
            count=Count('id')
        ).order_by('month', 'emotion_primary')

        # Organize data into a suitable format for charting
        trends_data = defaultdict(lambda: defaultdict(int))
        
        for item in monthly_posts:
            # Format month to 'YYYY-MM' or 'MMM YYYY'
            month_str = item['month'].strftime('%Y-%m') # e.g., "2025-01"
            emotion_name = item['emotion_primary'].capitalize()
            trends_data[month_str][emotion_name] = item['count']

        # Convert to list of dictionaries, ensuring consistent keys
        result = []
        all_emotions = sorted(list(set(e.capitalize() for e in Post.objects.values_list('emotion_primary', flat=True).distinct())))
        
        # Sort months chronologically
        sorted_months = sorted(trends_data.keys())

        for month_str in sorted_months:
            row = {'date': month_str} # Using 'date' as key as seen in frontend mock
            for emotion in all_emotions:
                row[emotion] = trends_data[month_str][emotion]
            result.append(row)

        return Response(result)

class AverageSentimentAPIView(views.APIView):
    """
    API endpoint to get the average sentiment score across all posts.
    """
    def get(self, request, *args, **kwargs):
        # Calculate the average of emotion_score
        avg_sentiment = Post.objects.aggregate(average_score=Avg('emotion_score'))['average_score']
        
        # Return a rounded average, or 0 if no posts
        avg_sentiment = round(avg_sentiment, 4) if avg_sentiment is not None else 0.0
        
        return Response({"average_sentiment_score": avg_sentiment})

class ActivePlatformsAPIView(views.APIView):
    """
    API endpoint to identify active platforms based on post count.
    Returns platforms sorted by post count.
    """
    def get(self, request, *args, **kwargs):
        platform_counts = Post.objects.values('platform').annotate(
            post_count=Count('id')
        ).order_by('-post_count') # Order by count descending

        # Convert to a list of dicts for the response
        result = [
            {'platform': item['platform'], 'post_count': item['post_count']}
            for item in platform_counts
        ]
        
        return Response(result)

class PlatformDistributionAPIView(views.APIView):
    """
    API endpoint to get the distribution of posts across different platforms.
    """
    def get(self, request, *args, **kwargs):
        platform_distribution = Post.objects.values('platform').annotate(
            count=Count('id')
        ).order_by('-count')

        # Define some example colors for platforms if not already handled by frontend
        platform_colors = {
            'X': '#000000',
            'Instagram': '#E1306C',
            'Facebook': '#1877F2',
            'YouTube': '#FF0000',
            'Reddit': '#FF4500',
        }

        distribution = []
        for item in platform_distribution:
            platform_name = item['platform']
            distribution.append({
                'name': platform_name.capitalize(), # Capitalize for display
                'value': item['count'],
                'color': platform_colors.get(platform_name, '#CCCCCC') # Default gray if no color
            })
        
        return Response(distribution)

class TopEmotionsByPlatformAPIView(views.APIView):
    """
    API endpoint to get the top primary emotion for each platform.
    """
    def get(self, request, *args, **kwargs):
        # Subquery to find the most common emotion for each platform
        # This is a bit complex in Django ORM for "top-1 per group"
        # A more straightforward approach for smaller datasets is to iterate
        
        platforms = Post.objects.values_list('platform', flat=True).distinct()
        result = []

        for platform in platforms:
            emotion_counts = Post.objects.filter(platform=platform)\
                                       .values('emotion_primary')\
                                       .annotate(count=Count('id'))\
                                       .order_by('-count')\
                                       .first() # Get the top emotion for this platform
            
            if emotion_counts:
                result.append({
                    'platform': platform.capitalize(),
                    'top_emotion': emotion_counts['emotion_primary'].capitalize(),
                    'count': emotion_counts['count']
                })
        
        # Sort the results by platform name for consistency
        result_sorted = sorted(result, key=lambda x: x['platform'])

        return Response(result_sorted)