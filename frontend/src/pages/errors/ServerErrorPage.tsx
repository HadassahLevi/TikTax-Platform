import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ServerCrash, Home, RefreshCw } from 'lucide-react';
import Button from '@/components/ui/Button';

/**
 * 500 Server Error Page
 * 
 * Displayed when the server encounters an internal error.
 * Provides retry functionality and clear error information.
 * 
 * @component
 */
export const ServerErrorPage: React.FC = () => {
  const navigate = useNavigate();

  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* Illustration */}
        <div className="mb-8">
          <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <ServerCrash className="w-12 h-12 text-red-600" />
          </div>
          <h1 className="text-6xl font-bold text-gray-900 mb-4">500</h1>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            משהו השתבש
          </h2>
          <p className="text-gray-600 mb-8">
            מצטערים, נתקלנו בבעיה טכנית. הצוות שלנו כבר עובד על פתרון. נסה שוב בעוד מספר דקות.
          </p>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <Button
            onClick={handleRetry}
            fullWidth
            size="lg"
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

        {/* Support Info */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-700">
            <strong>קוד שגיאה:</strong> 500 - Internal Server Error
          </p>
          <p className="text-sm text-gray-600 mt-2">
            אם הבעיה ממשיכה,{' '}
            <a href="mailto:support@tiktax.co.il" className="text-primary-600 hover:underline">
              צור קשר עם התמיכה
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};
