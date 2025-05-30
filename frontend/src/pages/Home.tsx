
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-platform-twitter/10 via-platform-instagram/10 to-platform-reddit/10 z-0" />
        <div className="absolute top-20 left-10 w-72 h-72 bg-platform-twitter/20 rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-80 h-80 bg-platform-instagram/20 rounded-full blur-3xl" />
        
        <div className="container mx-auto relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-platform-twitter via-platform-instagram to-platform-reddit bg-clip-text text-transparent">
              Track & Visualize Emotions Across Social Media
            </h1>
            <p className="text-lg md:text-xl mb-8 text-muted-foreground">
              Advanced AI-powered analytics to understand the emotional tone of conversations happening on social platforms in real-time.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button asChild size="lg" className="bg-gradient-to-r from-platform-twitter to-platform-instagram hover:opacity-90">
                <Link to="/dashboard">
                  Explore Dashboard
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to="/analytics">
                  View Analytics
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold mb-12 text-center">
            Powerful Emotion Analytics
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="glass-card overflow-hidden hover:shadow-xl transition-all duration-300">
              <div className="h-1 bg-platform-twitter" />
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-platform-twitter/20 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 22s8-4 8-10V7l-8-5-8 5v5c0 6 8 10 8 10" />
                  </svg>
                </div>
                <h3 className="text-xl font-medium mb-2">Real-time Tracking</h3>
                <p className="text-muted-foreground">
                  Monitor emotions across social platforms in real-time with advanced sentiment analysis.
                </p>
              </CardContent>
            </Card>
            
            <Card className="glass-card overflow-hidden hover:shadow-xl transition-all duration-300">
              <div className="h-1 bg-platform-instagram" />
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-platform-instagram/20 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M2 12h5" /><path d="M17 12h5" /><path d="M12 2v5" /><path d="M12 17v5" />
                    <circle cx="12" cy="12" r="7"></circle>
                  </svg>
                </div>
                <h3 className="text-xl font-medium mb-2">Comprehensive Analysis</h3>
                <p className="text-muted-foreground">
                  Gain insights into the emotional distribution and trends across different platforms.
                </p>
              </CardContent>
            </Card>
            
            <Card className="glass-card overflow-hidden hover:shadow-xl transition-all duration-300">
              <div className="h-1 bg-platform-facebook" />
              <CardContent className="p-6">
                <div className="w-12 h-12 rounded-full bg-platform-facebook/20 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 8.5V15c0 3-1.79 4-4 4H6c-2.21 0-4-1-4-4V8.5c0-3 1.79-4.5 4-4.5h2a2 2 0 0 1 2 2v.5A2 2 0 0 0 12 8h2a2 2 0 0 0 2-1.5V6a2 2 0 0 1 2-2h0c2.21 0 4 1.5 4 4.5Z" /><path d="M8 10v6" /><path d="M16 10v6" /><path d="M12 10v6" />
                  </svg>
                </div>
                <h3 className="text-xl font-medium mb-2">Visual Reports</h3>
                <p className="text-muted-foreground">
                  Beautiful, interactive charts and graphs to help you understand emotional patterns.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-16 px-4 bg-gradient-to-r from-secondary/50 to-secondary/30">
        <div className="container mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-6">
            Ready to understand the emotions behind social conversations?
          </h2>
          <p className="text-lg mb-8 text-muted-foreground max-w-2xl mx-auto">
            Start tracking emotions across social media platforms and gain valuable insights today.
          </p>
          <Button asChild size="lg" className="bg-gradient-to-r from-platform-twitter to-platform-instagram hover:opacity-90">
            <Link to="/dashboard">
              Go to Dashboard
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
