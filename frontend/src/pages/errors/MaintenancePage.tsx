import React from 'react';
import { Construction, Clock } from 'lucide-react';

/**
 * Maintenance Mode Page
 * 
 * Displayed when the system is undergoing scheduled maintenance.
 * Shows estimated downtime and update information.
 * 
 * @component
 */
export const MaintenancePage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-blue-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* Illustration */}
        <div className="mb-8">
          <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <Construction className="w-12 h-12 text-primary-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            תחזוקה מתוזמנת
          </h1>
          <p className="text-gray-600 mb-8">
            אנחנו משדרגים את המערכת כדי לשפר את החוויה שלך. נחזור בקרוב!
          </p>
        </div>

        {/* Estimated Time */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Clock className="w-5 h-5 text-primary-600" />
            <span className="font-semibold text-gray-900">זמן משוער לחזרה</span>
          </div>
          <p className="text-3xl font-bold text-primary-600">30 דקות</p>
          <p className="text-sm text-gray-600 mt-2">
            עדכון אחרון: {new Date().toLocaleTimeString('he-IL')}
          </p>
        </div>

        {/* Updates Section */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-900 mb-3">מה חדש?</h3>
          <ul className="text-right text-sm text-gray-600 space-y-2">
            <li>• שיפורים בביצועי המערכת</li>
            <li>• תיקוני באגים ויציבות</li>
            <li>• עדכוני אבטחה</li>
          </ul>
        </div>

        {/* Contact */}
        <p className="text-sm text-gray-600 mt-8">
          שאלות? צור קשר:{' '}
          <a href="mailto:support@tiktax.co.il" className="text-primary-600 hover:underline">
            support@tiktax.co.il
          </a>
        </p>
      </div>
    </div>
  );
};
