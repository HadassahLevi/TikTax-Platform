/**
 * Button Component Demo
 * 
 * This file demonstrates all the variations and use cases of the Button component.
 * Use this as a reference for implementing buttons throughout the Tik-Tax application.
 */

import React, { useState } from 'react';
import { Button } from '@/components/ui';
import { 
  Upload, 
  Download, 
  Trash2, 
  Plus, 
  Save, 
  X,
  Check,
  Eye,
  Edit,
  Calendar
} from 'lucide-react';

const ButtonDemo: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const simulateLoading = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="p-8 space-y-12 max-w-6xl mx-auto" dir="rtl">
      <header>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Button Component Demo
        </h1>
        <p className="text-gray-600">
          Comprehensive showcase of the Tik-Tax Button component following the design system
        </p>
      </header>

      {/* Variants */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Variants
        </h2>
        <div className="flex flex-wrap gap-4">
          <Button variant="primary">Primary - שמור</Button>
          <Button variant="secondary">Secondary - ביטול</Button>
          <Button variant="ghost">Ghost - עוד פרטים</Button>
          <Button variant="danger">Danger - מחק</Button>
        </div>
      </section>

      {/* Sizes */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Sizes
        </h2>
        <div className="flex flex-wrap items-end gap-4">
          <Button size="sm" variant="primary">Small - קטן</Button>
          <Button size="md" variant="primary">Medium - בינוני</Button>
          <Button size="lg" variant="primary">Large - גדול</Button>
        </div>
      </section>

      {/* With Icons */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          With Icons
        </h2>
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Icon Left</h3>
            <div className="flex flex-wrap gap-3">
              <Button icon={<Upload />} iconPosition="left">
                העלה קבלה
              </Button>
              <Button variant="secondary" icon={<Download />} iconPosition="left">
                הורד דוח
              </Button>
              <Button variant="ghost" icon={<Eye />} iconPosition="left">
                צפה
              </Button>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Icon Right</h3>
            <div className="flex flex-wrap gap-3">
              <Button icon={<Calendar />} iconPosition="right">
                בחר תאריך
              </Button>
              <Button variant="secondary" icon={<Plus />} iconPosition="right">
                הוסף עוד
              </Button>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Different Sizes with Icons</h3>
            <div className="flex flex-wrap items-end gap-3">
              <Button size="sm" icon={<Save />}>שמור</Button>
              <Button size="md" icon={<Save />}>שמור</Button>
              <Button size="lg" icon={<Save />}>שמור</Button>
            </div>
          </div>
        </div>
      </section>

      {/* States */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          States
        </h2>
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Loading State</h3>
            <div className="flex flex-wrap gap-3">
              <Button loading variant="primary">מעבד...</Button>
              <Button loading variant="secondary">שומר...</Button>
              <Button loading variant="danger">מוחק...</Button>
              <Button 
                variant="primary" 
                loading={isLoading} 
                onClick={simulateLoading}
              >
                לחץ לטעינה
              </Button>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">Disabled State</h3>
            <div className="flex flex-wrap gap-3">
              <Button disabled variant="primary">לא זמין</Button>
              <Button disabled variant="secondary">לא זמין</Button>
              <Button disabled variant="ghost">לא זמין</Button>
              <Button disabled variant="danger">לא זמין</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Full Width */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Full Width
        </h2>
        <div className="space-y-3 max-w-md">
          <Button fullWidth variant="primary">
            שמור שינויים
          </Button>
          <Button fullWidth variant="secondary">
            ביטול
          </Button>
          <Button fullWidth variant="ghost">
            למידע נוסף
          </Button>
        </div>
      </section>

      {/* Common Patterns */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Common Usage Patterns
        </h2>
        
        <div className="space-y-6">
          {/* Receipt Upload */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Receipt Upload (Primary Use Case)
            </h3>
            <Button 
              variant="primary" 
              size="lg" 
              icon={<Upload />}
              fullWidth
            >
              העלה קבלה חדשה
            </Button>
          </div>

          {/* Action Group */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Action Button Group
            </h3>
            <div className="flex gap-3">
              <Button variant="primary" icon={<Save />}>
                שמור
              </Button>
              <Button variant="secondary" icon={<X />}>
                ביטול
              </Button>
            </div>
          </div>

          {/* Mobile Stack */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Mobile Stacked Buttons
            </h3>
            <div className="flex flex-col gap-2 max-w-md">
              <Button fullWidth variant="primary">
                פעולה ראשית
              </Button>
              <Button fullWidth variant="secondary">
                פעולה משנית
              </Button>
              <Button fullWidth variant="ghost">
                ביטול
              </Button>
            </div>
          </div>

          {/* Destructive Action */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Destructive Action Confirmation
            </h3>
            <div className="flex gap-3">
              <Button variant="danger" size="sm" icon={<Trash2 />}>
                מחק קבלה
              </Button>
              <Button variant="secondary" size="sm">
                ביטול
              </Button>
            </div>
          </div>

          {/* Form Actions */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Form Submit/Cancel
            </h3>
            <form onSubmit={(e) => e.preventDefault()} className="space-y-3">
              <div className="flex gap-3 justify-end">
                <Button type="submit" variant="primary" icon={<Check />}>
                  שלח טופס
                </Button>
                <Button type="button" variant="ghost">
                  ביטול
                </Button>
              </div>
            </form>
          </div>

          {/* Edit/Delete Actions */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              Item Actions (Edit/Delete)
            </h3>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm" icon={<Edit />}>
                ערוך
              </Button>
              <Button variant="ghost" size="sm" icon={<Trash2 />}>
                מחק
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Accessibility */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Accessibility Features
        </h2>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 space-y-3">
          <div className="flex items-start gap-3">
            <Check className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900">Keyboard Navigation</p>
              <p className="text-sm text-blue-700">Tab, Enter, and Space key support</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <Check className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900">Focus Indicators</p>
              <p className="text-sm text-blue-700">Visible focus ring on keyboard navigation</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <Check className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900">ARIA Attributes</p>
              <p className="text-sm text-blue-700">aria-disabled and aria-busy automatically applied</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <Check className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900">Touch Targets</p>
              <p className="text-sm text-blue-700">Minimum 44px height for mobile accessibility</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ButtonDemo;
