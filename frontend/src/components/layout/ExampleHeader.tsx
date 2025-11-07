import React from 'react';
import { NotificationCenter } from '@/components/NotificationCenter';
import { Settings, User } from 'lucide-react';

/**
 * Example Header Component with Notification Center
 * 
 * This demonstrates how to integrate the NotificationCenter
 * into your app's header/navigation bar.
 */
export const ExampleHeader: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-blue-600">TikTax</h1>
          </div>

          {/* Right side actions */}
          <div className="flex items-center gap-2">
            {/* Notification Center - Bell Icon with Badge */}
            <NotificationCenter />

            {/* Settings Icon */}
            <button
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="הגדרות"
            >
              <Settings className="w-6 h-6 text-gray-700" />
            </button>

            {/* Profile Icon */}
            <button
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="פרופיל"
            >
              <User className="w-6 h-6 text-gray-700" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

/**
 * Usage in your app:
 * 
 * import { ExampleHeader } from '@/components/layout/ExampleHeader';
 * 
 * function App() {
 *   return (
 *     <div>
 *       <ExampleHeader />
 *       <main>{/* Your content *\/}</main>
 *     </div>
 *   );
 * }
 */
