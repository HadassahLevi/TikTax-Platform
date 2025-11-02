import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { BottomNav } from './BottomNav';

/**
 * BottomNav Component Demo
 * 
 * Demonstrates:
 * 1. Basic usage with export handler
 * 2. Active route highlighting
 * 3. Mobile-only visibility
 * 4. Elevated center button
 * 5. Proper page layout with padding
 */

export const BottomNavDemo: React.FC = () => {
  const [exportModalOpen, setExportModalOpen] = useState(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        {/* Demo Instructions Banner */}
        <div className="bg-primary-600 text-white p-4 text-center">
          <p className="text-sm font-medium">
            📱 Resize window to &lt;768px to see Bottom Navigation
          </p>
          <p className="text-xs mt-1">
            Desktop users: Open DevTools responsive mode
          </p>
        </div>

        {/* Main Content Area */}
        <main className="pb-20 md:pb-0 p-4">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Demo Section 1: Navigation Info */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Bottom Navigation Demo
              </h2>
              <p className="text-gray-600 mb-4">
                The bottom navigation bar appears only on mobile devices (screens smaller than 768px).
              </p>
              
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span><strong>Home:</strong> Navigate to Dashboard</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span><strong>Archive:</strong> View all receipts</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span><strong>+ (Center):</strong> Add new receipt (elevated button)</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span><strong>Export:</strong> Triggers export modal</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span><strong>Profile:</strong> User profile page</span>
                </div>
              </div>
            </div>

            {/* Demo Section 2: Features */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Features
              </h3>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 bg-success-50 rounded-lg">
                  <h4 className="font-semibold text-success-900 mb-2">
                    ✅ Responsive Design
                  </h4>
                  <p className="text-sm text-gray-700">
                    Automatically hides on desktop (≥768px) and shows on mobile (&lt;768px)
                  </p>
                </div>

                <div className="p-4 bg-info-50 rounded-lg">
                  <h4 className="font-semibold text-info-900 mb-2">
                    ✅ Active State
                  </h4>
                  <p className="text-sm text-gray-700">
                    Current route is highlighted with primary blue color and icon scaling
                  </p>
                </div>

                <div className="p-4 bg-warning-50 rounded-lg">
                  <h4 className="font-semibold text-warning-900 mb-2">
                    ✅ Elevated Center
                  </h4>
                  <p className="text-sm text-gray-700">
                    Primary action button floats 20px above nav bar with gradient and shadow
                  </p>
                </div>

                <div className="p-4 bg-primary-50 rounded-lg">
                  <h4 className="font-semibold text-primary-900 mb-2">
                    ✅ iOS Safe Area
                  </h4>
                  <p className="text-sm text-gray-700">
                    Respects iPhone notch with safe-area-inset-bottom support
                  </p>
                </div>
              </div>
            </div>

            {/* Demo Section 3: Styling Specs */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Styling Specifications
              </h3>
              
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Height:</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">64px</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Background:</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">White</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Border Top:</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">1px #E5E7EB</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Shadow:</span>
                  <code className="bg-gray-100 px-2 py-1 rounded text-xs">0 -2px 8px rgba(0,0,0,0.08)</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Icon Size (regular):</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">24px</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Icon Size (center):</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">28px</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Center Button Size:</span>
                  <code className="bg-gray-100 px-2 py-1 rounded">64px × 64px</code>
                </div>
                <div className="flex justify-between items-center border-b pb-2">
                  <span className="font-medium">Active Color:</span>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-primary-600 rounded"></div>
                    <code className="bg-gray-100 px-2 py-1 rounded">#2563EB</code>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-medium">Inactive Color:</span>
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 bg-gray-500 rounded"></div>
                    <code className="bg-gray-100 px-2 py-1 rounded">#6B7280</code>
                  </div>
                </div>
              </div>
            </div>

            {/* Demo Section 4: Export Modal Simulation */}
            {exportModalOpen && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[100]">
                <div className="bg-white rounded-lg shadow-xl p-6 max-w-md mx-4">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    Export Modal Triggered
                  </h3>
                  <p className="text-gray-600 mb-6">
                    This modal was opened by clicking the Export button in the bottom navigation.
                  </p>
                  <button
                    onClick={() => setExportModalOpen(false)}
                    className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                  >
                    Close Modal
                  </button>
                </div>
              </div>
            )}

            {/* Filler Content to Show Scrolling */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                Scroll Test
              </h3>
              <p className="text-gray-600 mb-4">
                The bottom navigation is fixed and stays at the bottom even when scrolling.
              </p>
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="mb-4 p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-medium text-gray-900 mb-2">Content Block {i}</h4>
                  <p className="text-sm text-gray-600">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco.
                  </p>
                </div>
              ))}
            </div>

            {/* Padding Info */}
            <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
              <p className="text-sm text-warning-900">
                <strong>⚠️ Important:</strong> Notice the <code className="bg-warning-100 px-1 rounded">pb-20</code> class 
                on the main element. This prevents the bottom navigation from covering content on mobile.
              </p>
            </div>
          </div>
        </main>

        {/* Bottom Navigation */}
        <BottomNav 
          onExportClick={() => setExportModalOpen(true)}
        />
      </div>
    </BrowserRouter>
  );
};

// Usage Example Code (for documentation)
export const usageExample = `
import { BottomNav } from '@/components/layout';
import { useState } from 'react';

function App() {
  const [exportModalOpen, setExportModalOpen] = useState(false);

  return (
    <>
      {/* Main content with bottom padding for mobile */}
      <main className="pb-20 md:pb-0">
        {/* Your page content here */}
      </main>

      {/* Bottom Navigation (mobile-only) */}
      <BottomNav 
        onExportClick={() => setExportModalOpen(true)}
      />
    </>
  );
}
`;
