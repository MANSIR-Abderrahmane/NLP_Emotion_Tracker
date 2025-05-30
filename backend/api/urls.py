from django.urls import path
from . import views

urlpatterns = [
    # Post related URLs
    path('posts/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

    # Emotion and Platform Analytics URLs
    path('emotion-distribution/', views.EmotionDistributionAPIView.as_view(), name='emotion-distribution'),
    path('emotion-trends/', views.EmotionTrendAPIView.as_view(), name='emotion-trends'),
    path('average-sentiment/', views.AverageSentimentAPIView.as_view(), name='average-sentiment'),
    path('active-platforms/', views.ActivePlatformsAPIView.as_view(), name='active-platforms'),
    path('platform-distribution/', views.PlatformDistributionAPIView.as_view(), name='platform-distribution'),
    path('top-emotions-by-platform/', views.TopEmotionsByPlatformAPIView.as_view(), name='top-emotions-by-platform'),
]