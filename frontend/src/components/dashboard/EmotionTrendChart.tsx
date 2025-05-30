
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TrendData {
  date: string;
  happy: number;
  sad: number;
  angry: number;
  surprised: number;
  neutral: number;
}

interface EmotionTrendChartProps {
  data: TrendData[];
}

const EmotionTrendChart: React.FC<EmotionTrendChartProps> = ({ data }) => {
  return (
    <div className="w-full h-full min-h-[300px]">
      <h3 className="font-medium mb-4">Emotion Trends Over Time</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="date" stroke="#999" />
          <YAxis stroke="#999" />
          <Tooltip 
            contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="happy" 
            stroke="#4FD1C5" 
            activeDot={{ r: 8 }} 
            strokeWidth={2}
            className="animate-pulse-soft" 
          />
          <Line 
            type="monotone" 
            dataKey="sad" 
            stroke="#8884D8" 
            strokeWidth={2} 
            className="animate-pulse-soft" 
          />
          <Line 
            type="monotone" 
            dataKey="angry" 
            stroke="#F56565" 
            strokeWidth={2} 
            className="animate-pulse-soft" 
          />
          <Line 
            type="monotone" 
            dataKey="surprised" 
            stroke="#ED8936" 
            strokeWidth={2} 
            className="animate-pulse-soft" 
          />
          <Line 
            type="monotone" 
            dataKey="neutral" 
            stroke="#90CDF4" 
            strokeWidth={2} 
            className="animate-pulse-soft" 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EmotionTrendChart;
