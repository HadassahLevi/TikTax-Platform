import React from 'react';
import { useToast } from '@/contexts/ToastContext';
import { NotificationCenter } from '@/components/NotificationCenter';

/**
 * Demo page for testing notification system
 * Shows toast examples and notification center
 */
export const NotificationDemo: React.FC = () => {
  const { showToast } = useToast();

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Notification System Demo</h1>
            <p className="text-gray-600 mt-2">Test toast messages and notification center</p>
          </div>
          <NotificationCenter />
        </div>

        {/* Toast Examples */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Toast Messages</h2>
          <p className="text-gray-600 mb-4">Click buttons to show temporary toast notifications</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() =>
                showToast({
                  type: 'success',
                  title: 'הצלחה!',
                  message: 'הקבלה נשמרה בהצלחה בארכיון'
                })
              }
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              Success Toast
            </button>

            <button
              onClick={() =>
                showToast({
                  type: 'error',
                  title: 'שגיאה',
                  message: 'לא ניתן לעבד את הקבלה. נסה שוב.'
                })
              }
              className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Error Toast
            </button>

            <button
              onClick={() =>
                showToast({
                  type: 'warning',
                  title: 'אזהרה',
                  message: 'השתמשת ב-85% ממכסת הקבלות החודשית'
                })
              }
              className="px-6 py-3 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
            >
              Warning Toast
            </button>

            <button
              onClick={() =>
                showToast({
                  type: 'info',
                  title: 'מידע',
                  message: 'המנוי שלך יפוג בעוד 7 ימים'
                })
              }
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Info Toast
            </button>

            <button
              onClick={() =>
                showToast({
                  type: 'success',
                  title: 'קצר',
                  message: 'הודעה קצרה',
                  duration: 2000
                })
              }
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Short Duration (2s)
            </button>

            <button
              onClick={() =>
                showToast({
                  type: 'info',
                  title: 'ארוך',
                  message: 'הודעה עם משך זמן ארוך יותר',
                  duration: 10000
                })
              }
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Long Duration (10s)
            </button>
          </div>
        </div>

        {/* Notification Center Info */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Notification Center</h2>
          <p className="text-gray-600 mb-4">Click the bell icon in the top right to:</p>
          
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            <li>View all notifications</li>
            <li>See unread count badge</li>
            <li>Mark individual notifications as read</li>
            <li>Mark all as read at once</li>
            <li>Delete individual notifications</li>
            <li>Click on notifications to navigate (if action URL exists)</li>
            <li>Auto-refresh every 30 seconds</li>
          </ul>
        </div>

        {/* Testing Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-blue-900 mb-4">Testing Instructions</h2>
          
          <div className="space-y-4 text-blue-900">
            <div>
              <h3 className="font-semibold mb-2">1. Backend Notifications</h3>
              <p className="text-sm">Run in terminal:</p>
              <code className="block bg-blue-100 p-2 rounded mt-2 text-xs">
                cd backend && python test_notifications_manual.py
              </code>
            </div>

            <div>
              <h3 className="font-semibold mb-2">2. Toast Messages</h3>
              <p className="text-sm">Click the buttons above to test different toast types</p>
            </div>

            <div>
              <h3 className="font-semibold mb-2">3. Notification Center</h3>
              <p className="text-sm">Click the bell icon to open the notification panel</p>
            </div>

            <div>
              <h3 className="font-semibold mb-2">4. Integration Test</h3>
              <p className="text-sm">Upload a receipt to see real notifications created automatically</p>
            </div>
          </div>
        </div>

        {/* API Reference */}
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-semibold mb-4">Quick API Reference</h2>
          
          <div className="space-y-4 text-sm">
            <div>
              <code className="text-blue-600">GET /notifications</code>
              <p className="text-gray-600 ml-4">Get user notifications (paginated)</p>
            </div>
            
            <div>
              <code className="text-blue-600">GET /notifications/unread-count</code>
              <p className="text-gray-600 ml-4">Get unread notification count</p>
            </div>
            
            <div>
              <code className="text-blue-600">PUT /notifications/:id/read</code>
              <p className="text-gray-600 ml-4">Mark notification as read</p>
            </div>
            
            <div>
              <code className="text-blue-600">POST /notifications/mark-all-read</code>
              <p className="text-gray-600 ml-4">Mark all as read</p>
            </div>
            
            <div>
              <code className="text-blue-600">DELETE /notifications/:id</code>
              <p className="text-gray-600 ml-4">Delete notification</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
