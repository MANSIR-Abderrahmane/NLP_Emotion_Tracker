// frontend/src/pages/Analytics.tsx

import React, { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell, PieChart, Pie, Legend } from 'recharts';
import axios from 'axios';

const emotionColors = {
  Joy: '#4FD1C5',
  Sadness: '#8884D8',
  Anger: '#F56565',
  Surprise: '#ED8936',
  Neutral: '#90CDF4',
  Fear: '#9F7AEA',
  Love: '#FF69B4',
  Disgust: '#48BB78',
};

const platformChartColors = ['#36A2EB', '#E1306C', '#1877F2', '#FF0000', '#FF4500'];

const Analytics: React.FC = () => {
  const [emotionDistributionData, setEmotionDistributionData] = useState<any[]>([]);
  const [emotionTrendData, setEmotionTrendData] = useState<any[]>([]);
  const [platformDistributionData, setPlatformDistributionData] = useState<any[]>([]);
  const [topEmotionsByPlatform, setTopEmotionsByPlatform] = useState<any[]>([]); // New state for this data
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        const emotionDistResponse = await axios.get('http://127.0.0.1:8000/api/emotion-distribution/');
        setEmotionDistributionData(emotionDistResponse.data);

        const emotionTrendsResponse = await axios.get('http://127.0.0.1:8000/api/emotion-trends/');
        setEmotionTrendData(emotionTrendsResponse.data);

        const platformDistResponse = await axios.get('http://127.0.0.1:8000/api/platform-distribution/');
        setPlatformDistributionData(platformDistResponse.data);

        // Fetch Top Emotions by Platform Data (assuming a new API endpoint for this)
        const topEmotionsByPlatformResponse = await axios.get('http://127.0.0.1:8000/api/top-emotions-by-platform/');
        setTopEmotionsByPlatform(topEmotionsByPlatformResponse.data);


        setLoading(false);
      } catch (err) {
        setError('Failed to fetch analytics data. Please ensure the backend is running and accessible.');
        setLoading(false);
        console.error("Error fetching analytics data:", err);
      }
    };

    fetchAnalyticsData();
  }, []);

  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto p-6">
          <Card className="glass-card p-6 text-center">
            <CardContent>
              <p>Loading analytics data...</p>
            </CardContent>
          </Card>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="container mx-auto p-6">
          <Card className="glass-card p-6 text-center">
            <CardContent>
              <p className="text-red-500">{error}</p>
            </CardContent>
          </Card>
        </div>
      </Layout>
    );
  }

  const emotionTrendKeys = emotionTrendData.length > 0
    ? Object.keys(emotionTrendData[0]).filter(key => key !== 'time')
    : [];

  // Determine keys for top emotions by platform dynamically
  const topEmotionKeys = topEmotionsByPlatform.length > 0
    ? Object.keys(topEmotionsByPlatform[0]).filter(key => key !== 'platform')
    : [];


  return (
    <Layout>
      <div className="container mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-8">Emotion Analytics</h1>
        
        <Tabs defaultValue="overview" className="w-full">
          <TabsList className="grid w-full md:w-auto grid-cols-3 mb-8">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="platforms">Platforms</TabsTrigger>
            <TabsTrigger value="trends">Trends</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <Card className="glass-card overflow-hidden">
                <div className="p-4 border-b border-border">
                  <h3 className="font-medium text-center">Platform Distribution</h3>
                </div>
                <CardContent className="p-4">
                  <div className="h-[300px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={platformDistributionData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {platformDistributionData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={platformChartColors[index % platformChartColors.length]} />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value: number, name: string) => [`${value} posts`, name]}
                          contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                        />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              <Card className="glass-card overflow-hidden">
                <div className="p-4 border-b border-border">
                  <h3 className="font-medium text-center">Emotion Trends Over Time</h3>
                </div>
                <CardContent className="p-4">
                  <div className="h-[300px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart
                        data={emotionTrendData}
                        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                        <XAxis dataKey="time" stroke="#999" />
                        <YAxis stroke="#999" />
                        <Tooltip
                          contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                        />
                        <Legend />
                        {emotionTrendKeys.map(key => (
                          <Area
                            key={key}
                            type="monotone"
                            dataKey={key}
                            stackId="1"
                            stroke={(emotionColors as any)[key]}
                            fill={(emotionColors as any)[key]}
                            fillOpacity={0.3}
                          />
                        ))}
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="glass-card overflow-hidden">
              <div className="p-4 border-b border-border">
                <h3 className="font-medium text-center">Top Emotions by Platform</h3>
              </div>
              <CardContent className="p-4">
                <div className="h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={topEmotionsByPlatform}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="platform" stroke="#999" />
                      <YAxis stroke="#999" />
                      <Tooltip
                        contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                      />
                      <Legend />
                      <Bar dataKey="Happy" stackId="a" fill={emotionColors.Joy} />
                      <Bar dataKey="Sad" stackId="a" fill={emotionColors.Sadness} />
                      <Bar dataKey="Angry" stackId="a" fill={emotionColors.Anger} />
                      <Bar dataKey="Surprise" stackId="a" fill={emotionColors.Surprise} />
                      <Bar dataKey="Neutral" stackId="a" fill={emotionColors.Neutral} />
                      <Bar dataKey="Happy" stackId="a" fill={emotionColors.Fear} />
                      <Bar dataKey="Sad" stackId="a" fill={emotionColors.Love} />
                      <Bar dataKey="Angry" stackId="a" fill={emotionColors.Disgust} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="platforms" className="space-y-6">
            <Card className="glass-card overflow-hidden">
              <div className="p-4 border-b border-border">
                <h3 className="font-medium text-center">Platform Comparison</h3>
              </div>
              <CardContent className="p-4">
                <div className="h-[500px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={topEmotionsByPlatform}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                      layout="vertical"
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis type="number" stroke="#999" />
                      <YAxis dataKey="platform" type="category" stroke="#999" />
                      <Tooltip
                        contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                      />
                      <Legend />
                      {topEmotionKeys.map(key => (
                        <Bar key={key} dataKey={key} fill={(emotionColors as any)[key]} />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="trends" className="space-y-6">
            <Card className="glass-card overflow-hidden">
              <div className="p-4 border-b border-border">
                <h3 className="font-medium text-center">Emotion Trends Over Time</h3>
              </div>
              <CardContent className="p-4">
                <div className="h-[500px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                      data={emotionTrendData}
                      margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="time" stroke="#999" />
                      <YAxis stroke="#999" />
                      <Tooltip
                        contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
                      />
                      <Legend />
                      {emotionTrendKeys.map(key => (
                        <Area
                          key={key}
                          type="monotone"
                          dataKey={key}
                          stroke={(emotionColors as any)[key]}
                          fill={(emotionColors as any)[key]}
                          fillOpacity={0.3}
                        />
                      ))}
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
};

export default Analytics;