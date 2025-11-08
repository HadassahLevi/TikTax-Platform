import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { WifiOff, RefreshCw, Home } from 'lucide-react';
import Button from '@/components/ui/Button';

/**
 * Network Error Page
 * 
 * Displayed when there's no internet connection.
 * Automatically detects when connection is restored.
 * 
 * @component
 */
export const NetworkErrorPage: React.FC = () => {
  const navigate = useNavigate();
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleRetry = () => {
    if (navigator.onLine) {
      window.location.reload();
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* Illustration */}
        <div className="mb-8">
          <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 ${
            isOnline ? 'bg-green-100' : 'bg-amber-100'
          }`}>
            <WifiOff className={`w-12 h-12 ${isOnline ? 'text-green-600' : 'text-amber-600'}`} />
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            {isOnline ? 'החיבור חזר!' : 'בעיית חיבור לאינטרנט'}
          </h2>
          <p className="text-gray-600 mb-8">
            {isOnline 
              ? 'החיבור לאינטרנט חזר. לחץ על "נסה שוב" כדי להמשיך.'
              : 'נראה שיש בעיה בחיבור לאינטרנט שלך. בדוק את החיבור ונסה שוב.'
            }
          </p>
        </div>

        {/* Status Indicator */}
        <div className={`p-4 rounded-lg mb-6 ${
          isOnline ? 'bg-green-50 border border-green-200' : 'bg-amber-50 border border-amber-200'
        }`}>
          <div className="flex items-center justify-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              isOnline ? 'bg-green-500' : 'bg-amber-500'
            } animate-pulse`}></div>
            <span className={`text-sm font-medium ${
              isOnline ? 'text-green-800' : 'text-amber-800'
            }`}>
              {isOnline ? 'מחובר לאינטרנט' : 'לא מחובר לאינטרנט'}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <Button
            onClick={handleRetry}
            fullWidth
            size="lg"
            disabled={!isOnline}
            icon={<RefreshCw className="w-5 h-5" />}
          >
            נסה שוב
          </Button>
          
          <Button
            onClick={() => navigate('/dashboard')}
            variant="secondary"
            fullWidth
            size="lg"
            icon={<Home className="w-5 h-5" />}
          >
            חזור לדף הבית
          </Button>
        </div>

        {/* Tips */}
        <div className="mt-8 text-right">
          <h4 className="text-sm font-semibold text-gray-900 mb-2">טיפים לפתרון:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• בדוק שה-WiFi מחובר</li>
            <li>• נסה לאתחל את הראוטר</li>
            <li>• בדוק שהנתונים הסלולריים מופעלים</li>
            <li>• נסה להתחבר מרשת אחרת</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
