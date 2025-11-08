import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FileQuestion, Home, ArrowRight } from 'lucide-react';
import Button from '@/components/ui/Button';

/**
 * 404 Not Found Error Page
 * 
 * Displayed when user navigates to a non-existent route.
 * Provides clear messaging and navigation options.
 * 
 * @component
 */
export const NotFoundPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* Illustration */}
        <div className="mb-8">
          <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <FileQuestion className="w-12 h-12 text-primary-600" />
          </div>
          <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            הדף לא נמצא
          </h2>
          <p className="text-gray-600 mb-8">
            מצטערים, הדף שחיפשת לא קיים או שהוסר. אולי הקישור שגוי?
          </p>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <Button
            onClick={() => navigate('/dashboard')}
            fullWidth
            size="lg"
            icon={<Home className="w-5 h-5" />}
          >
            חזור לדף הבית
          </Button>
          
          <Button
            onClick={() => navigate(-1)}
            variant="secondary"
            fullWidth
            size="lg"
            icon={<ArrowRight className="w-5 h-5" />}
          >
            חזור לדף הקודם
          </Button>
        </div>

        {/* Help Text */}
        <p className="text-sm text-gray-500 mt-8">
          צריך עזרה?{' '}
          <a href="mailto:support@tiktax.co.il" className="text-primary-600 hover:underline">
            צור קשר עם התמיכה
          </a>
        </p>
      </div>
    </div>
  );
};
