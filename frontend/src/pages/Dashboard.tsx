// frontend/src/pages/Dashboard.tsx

import React, { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import { Card, CardContent } from '@/components/ui/card';
import PlatformSelector, { SocialPlatform } from '@/components/dashboard/PlatformSelector';
import EmotionDistributionChart from '@/components/dashboard/EmotionDistributionChart';
import EmotionTrendChart from '@/components/dashboard/EmotionTrendChart';
import PostCard, { Post } from '@/components/dashboard/PostCard'; // Ensure Post is imported
import StatCard from '@/components/dashboard/StatCard';
import axios from 'axios';
import { Button } from '@/components/ui/button';

const Dashboard = () => {
  const [selectedPlatform, setSelectedPlatform] = useState<SocialPlatform>('all');

  // State for fetched data
  const [emotionDistributionData, setEmotionDistributionData] = useState<any[]>([]);
  const [trendData, setTrendData] = useState<any[]>([]);
  const [totalPosts, setTotalPosts] = useState<number | null>(null);
  const [averageSentiment, setAverageSentiment] = useState<number | null>(null);
  const [activePlatformsCount, setActivePlatforms] = useState<any[]>([]);
  const [recentPosts, setRecentPosts] = useState<Post[]>([]); // State to hold fetched recent posts
  const [topPlatformDescription, setTopPlatformDescription] = useState<string>('Loading...');

  // --- Data Fetching useEffects ---
  useEffect(() => {
    // Fetch Emotion Distribution Data
    axios.get('http://127.0.0.1:8000/api/emotion-distribution/')
      .then(response => {
        setEmotionDistributionData(response.data);
      })
      .catch(error => console.error('Error fetching emotion distribution:', error));

    // Fetch Emotion Trend Data
    axios.get('http://127.0.0.1:8000/api/emotion-trends/')
      .then(response => {
        setTrendData(response.data);
      })
      .catch(error => console.error('Error fetching emotion trends:', error));

    // Fetch Total Posts Count
    axios.get('http://127.0.0.1:8000/api/posts/') // Using the /api/posts/ endpoint and then checking length
      .then(response => {
        setTotalPosts(response.data.length); // Assuming response.data is an array of posts
      })
      .catch(error => console.error('Error fetching total posts:', error));

    // Fetch Average Sentiment
    axios.get('http://127.0.0.1:8000/api/average-sentiment/')
      .then(response => {
        setAverageSentiment(response.data.average_sentiment);
      })
      .catch(error => console.error('Error fetching average sentiment:', error));

    // Fetch Active Platforms Count
    axios.get('http://127.0.0.1:8000/api/active-platforms/')
      .then(response => {
        setActivePlatforms(response.data.platform);
      })
      .catch(error => console.error('Error fetching active platforms:', error));

    // Fetch Recent Posts (for PostCard display)
    const fetchRecentPosts = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/posts/');
        // Assuming your API returns an array of post objects directly
        setRecentPosts(response.data);
      } catch (error) {
        console.error('Error fetching recent posts:', error);
        setRecentPosts([]); // Set to empty array on error
      }
    };
    fetchRecentPosts();
  }, []); // Empty dependency array means these effects run once on mount

  // --- Export Functions ---
  const handleExportPostsJSON = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/posts/');
      const postsToExport = response.data;

      const jsonString = JSON.stringify(postsToExport, null, 2); // Pretty print JSON

      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'posts_export.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      console.log('Posts exported as JSON.');
    } catch (error) {
      console.error('Error exporting posts as JSON:', error);
      alert('Failed to export posts as JSON. Check console for details.');
    }
  };

  const handleExportPostsCSV = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/posts/');
      const postsToExport: Post[] = response.data;

      if (postsToExport.length === 0) {
        alert('No posts to export.');
        return;
      }

      // Define CSV headers - adjust if you want more/fewer fields
      const headers = [
        'id', 'platform', 'author', 'date', 'content', 'likes',
        'emotion_primary', 'emotion_score', 'secondary_emotions_json', 'true_emotion_label'
      ];

      // Helper to escape values for CSV
      const escapeCsvValue = (value: any) => {
        if (value === null || value === undefined) return '';
        let stringValue = String(value);
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
          return `"${stringValue.replace(/"/g, '""')}"`;
        }
        return stringValue;
      };

      // Create CSV rows
      const csvRows = [
        headers.map(escapeCsvValue).join(',') // Header row
      ];

      postsToExport.forEach(post => {
        const row = headers.map(header => {
          if (header === 'secondary_emotions_json') {
            // Stringify the JSON object for CSV
            return escapeCsvValue(JSON.stringify(post[header]));
          }
          // Access properties directly from the post object
          return escapeCsvValue((post as any)[header]);
        });
        csvRows.push(row.join(','));
      });

      const csvString = csvRows.join('\n');
      const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'posts_export.csv';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      console.log('Posts exported as CSV.');
    } catch (error) {
      console.error('Error exporting posts as CSV:', error);
      alert('Failed to export posts as CSV. Check console for details.');
    }
  };

  return (
    <Layout>
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-8 text-center text-primary-dark">Social Media Sentiment Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Posts"
            // Change: Use typeof check for totalPosts
            value={typeof totalPosts === 'number' ? totalPosts.toString() : 'Loading...'}
            description="Overall number of analyzed posts"
            color="bg-blue-500"
            icon={<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z" /><path d="M16 2v4a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V2" /><path d="M8 22v-4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4" /></svg>}
          />
          <StatCard
            title="Average Sentiment Score"
            // Change: Use typeof check for averageSentiment
           value={typeof averageSentiment === 'number' ? averageSentiment.toFixed() : 'Loading...'}
            description="Overall emotional tone of posts (0-1)"
            color="bg-green-500"
            icon={<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><path d="M8 14s1.5 2 4 2 4-2 4-2" /><line x1="9" x2="9.01" y1="9" y2="9" /><line x1="15" x2="15.01" y1="9" y2="9" /></svg>}
          />
          <StatCard
            title="Most Frequent Emotion"
            value={emotionDistributionData.length > 0 ? emotionDistributionData[6].name : 'Loading...'}
            description="Dominant emotion across all posts"
            color="bg-purple-500"
            icon={<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2z" /><path d="M16 16s-1.5-2-4-2-4 2-4 2" /><line x1="9" x2="9.01" y1="9" y2="9" /><line x1="15" x2="15.01" y1="9" y2="9" /></svg>}
          />
          <StatCard
            title="Active Platforms"
            // Change: Use typeof check for activePlatformsCount
            value="Facebook"
            description={topPlatformDescription}
            color="bg-platform-facebook"
            icon={<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" /><path d="M12 8v8" /><path d="M8 12h8" /></svg>}
          />
        </div>

        <PlatformSelector
          selectedPlatform={selectedPlatform}
          onSelectPlatform={setSelectedPlatform}
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card className="glass-card p-4">
            <CardContent className="p-0">
              <EmotionDistributionChart data={emotionDistributionData} />
            </CardContent>
          </Card>

          <Card className="glass-card p-4">
            <CardContent className="p-0">
              <EmotionTrendChart data={trendData} />
            </CardContent>
          </Card>
        </div>

        {/* Export Buttons */}
        <div className="flex justify-end space-x-4 mb-6">
          <Button onClick={handleExportPostsJSON}>Export Posts (JSON)</Button>
          <Button onClick={handleExportPostsCSV}>Export Posts (CSV)</Button>
        </div>

        <h2 className="text-2xl font-bold mb-6">Recent Posts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recentPosts.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>

      </div>
    </Layout>
  );
};

export default Dashboard;