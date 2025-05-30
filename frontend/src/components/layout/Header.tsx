
import React from 'react';
import { NavLink } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 w-full bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-platform-twitter to-platform-instagram flex items-center justify-center">
            <span className="text-white font-bold text-sm">ET</span>
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-platform-twitter via-platform-instagram to-platform-reddit bg-clip-text text-transparent">
            Emotion Tracker
          </span>
        </div>
        
        <nav className="hidden md:flex items-center space-x-6">
          <NavLink 
            to="/" 
            className={({ isActive }) => 
              `text-sm font-medium transition-colors ${isActive 
                ? 'text-white' 
                : 'text-muted-foreground hover:text-white'}`
            }
            end
          >
            Home
          </NavLink>
          <NavLink 
            to="/dashboard" 
            className={({ isActive }) => 
              `text-sm font-medium transition-colors ${isActive 
                ? 'text-white' 
                : 'text-muted-foreground hover:text-white'}`
            }
          >
            Dashboard
          </NavLink>
          <NavLink 
            to="/analytics" 
            className={({ isActive }) => 
              `text-sm font-medium transition-colors ${isActive 
                ? 'text-white' 
                : 'text-muted-foreground hover:text-white'}`
            }
          >
            Analytics
          </NavLink>
        </nav>
        
        <div className="md:hidden">
          <button className="p-2 text-white rounded-md hover:bg-secondary/50">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
