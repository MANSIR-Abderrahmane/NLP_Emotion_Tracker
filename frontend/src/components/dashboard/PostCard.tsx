// frontend/src/components/dashboard/PostCard.tsx

import React from 'react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

// Updated Post Interface to match backend serializer
export interface Post {
  id: number; // Backend `id` is a number (BigAutoField)
  external_id?: string; // Optional, as it can be null/blank
  content: string;
  platform: string;
  author: string;
  date: string; // Date string from backend (ISO format)
  likes: number;
  emotion_primary: string; // Direct field from backend
  emotion_score: number;  // Direct field from backend
  secondary_emotions_json: { [key: string]: number }; // Backend sends this as a dictionary
  true_emotion_label?: string | null; // Optional, can be null/blank
}

interface PostCardProps {
  post: Post;
}

const platformColors = {
  twitter: 'bg-white/10',
  instagram: 'bg-platform-instagram',
  facebook: 'bg-platform-facebook',
  youtube: 'bg-platform-youtube',
  reddit: 'bg-platform-reddit'
};

const emotionColors = {
  joy: 'bg-green-500',
  sadness: 'bg-blue-500',
  anger: 'bg-red-500',
  surprise: 'bg-yellow-500',
  fear: 'bg-orange-500',
  love: 'bg-pink-500',
  error: 'bg-black/10', // Assuming 'error' is a fallback for unknown emotions
  neutral: 'bg-gray-300',
  disgust: 'bg-purple-500',
};

const PostCard: React.FC<PostCardProps> = ({ post }) => {
  // Calculate emotionColor using emotion_primary directly
  const emotionColor = (emotionColors as any)[post.emotion_primary.toLowerCase()] || 'bg-gray-500';

  // Transform secondary_emotions_json (dictionary) into an array of { name: string, score: number }
  // This matches the previous expected format for `secondaryEmotions` in the component.
  const secondaryEmotionsArray = Object.entries(post.secondary_emotions_json || {}).map(([name, score]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1), // Capitalize the first letter for display
    score: score,
  }));

  // Handle date formatting if needed (e.g., if you want 'DD/MM/YYYY HH:MM')
  // This is optional, depending on how you want to display the date.
  // Example:
  // const formattedDate = new Date(post.date).toLocaleString(); // Adjust locale and options as needed

  return (
    <Card className="glass-card flex flex-col h-full overflow-hidden">
      <div className={`h-1 ${platformColors[post.platform] || 'bg-gray-500'}`} />
      <CardContent className="p-4 flex-grow">
        <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
          <div className={`px-2 py-1 rounded-full text-xs font-semibold ${platformColors[post.platform.toLowerCase() as keyof typeof platformColors] || 'bg-black'}`}>
            {post.platform}
          </div>
          <span>{new Date(post.date).toLocaleString()}</span> {/* Display formatted date */}
        </div>
        <p className="text-sm text-gray-700 mb-4 flex-grow line-clamp-3">
          {post.content}
        </p>

        <div className="flex items-center justify-between">
          <Badge
            // Use post.emotion_primary directly for color and text
            className={`${(emotionColors as any)[post.emotion_primary.toLowerCase()] || 'bg-gray-500'}`}
          >
            {post.emotion_primary}
          </Badge>
          <span className="text-xs font-medium">
            {/* Use post.emotion_score directly */}
            {(post.emotion_score * 100).toFixed(0)}% Confidence
          </span>
        </div>

        <Progress
          // Use post.emotion_score directly for progress value
          value={post.emotion_score * 100}
          className={`mt-2 h-1 ${emotionColor}`}
        />
      </CardContent>

      <CardFooter className="px-4 py-3 bg-secondary/30 flex items-center justify-between">
        <span className="text-xs font-medium">@{post.author}</span>
        <div className="flex space-x-1.5">
          {/* Iterate over the transformed secondaryEmotionsArray */}
          {secondaryEmotionsArray.map((emotion) => (
            <div
              key={emotion.name}
              className="group relative"
            >
              <div
                className={`w-2 h-2 rounded-full ${(emotionColors as any)[emotion.name.toLowerCase()] || 'bg-gray-500'}`}
              />
              <div className="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2 bg-secondary/80 text-xs px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {emotion.name}: {(emotion.score * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </CardFooter>
    </Card>
  );
};

export default PostCard;