
import React from 'react';
import { Card } from '@/components/ui/card';

export type SocialPlatform = 'twitter' | 'instagram' | 'facebook' | 'youtube' | 'reddit' | 'all';

interface PlatformSelectorProps {
  selectedPlatform: SocialPlatform;
  onSelectPlatform: (platform: SocialPlatform) => void;
}

const PlatformSelector: React.FC<PlatformSelectorProps> = ({ 
  selectedPlatform, 
  onSelectPlatform 
}) => {
  const platforms = [
    { id: 'twitter', name: 'X', color: 'platform-twitter' },
    { id: 'instagram', name: 'Instagram', color: 'platform-instagram' },
    { id: 'facebook', name: 'Facebook', color: 'platform-facebook' },
    { id: 'youtube', name: 'YouTube', color: 'platform-youtube' },
    { id: 'reddit', name: 'Reddit', color: 'platform-reddit' },
  ];

  return (
    <div className="mb-6">
      <h3 className="font-medium mb-4">Filter by Platform</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
        <Card 
          className={`platform-card p-4 hover:bg-secondary/50 ${
            selectedPlatform === 'all' ? 'platform-card-active ring-white' : ''
          }`}
          onClick={() => onSelectPlatform('all')}
        >
          <div className="flex flex-col items-center justify-center">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-platform-twitter via-platform-instagram to-platform-reddit flex items-center justify-center mb-2">
              <span className="text-white font-bold">All</span>
            </div>
            <span className="text-xs font-medium">All Platforms</span>
          </div>
        </Card>
        
        {platforms.map((platform) => (
          <Card 
            key={platform.id}
            className={`platform-card p-4 hover:bg-secondary/50 ${
              selectedPlatform === platform.id ? `platform-card-active ring-${platform.color}` : ''
            }`}
            onClick={() => onSelectPlatform(platform.id as SocialPlatform)}
          >
            <div className="flex flex-col items-center justify-center">
              <div 
                className={`w-10 h-10 rounded-full bg-${platform.color} flex items-center justify-center mb-2 animate-float`}
                style={{ animationDelay: `${platforms.indexOf(platform) * 0.2}s` }}
              >
                <span className="text-white font-bold">{platform.name.charAt(0)}</span>
              </div>
              <span className="text-xs font-medium">{platform.name}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default PlatformSelector;
