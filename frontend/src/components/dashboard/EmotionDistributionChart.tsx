
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface EmotionData {
  name: string;
  value: number;
  color: string;
}

interface EmotionDistributionChartProps {
  data: EmotionData[];
}

const EmotionDistributionChart: React.FC<EmotionDistributionChartProps> = ({ data }) => {
  return (
    <div className="w-full h-full min-h-[300px]">
      <h3 className="font-medium mb-4">Emotion Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            className="animate-pulse-soft"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value: number) => [`${value}%`, 'Percentage']}
            contentStyle={{ background: '#1E1E1E', border: '1px solid #333', borderRadius: '8px' }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EmotionDistributionChart;
