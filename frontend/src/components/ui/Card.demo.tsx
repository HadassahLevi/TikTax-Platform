import React, { useState } from 'react';
import Card from './Card';

/**
 * Card Component Demo
 * 
 * Demonstrates all variants and usage patterns for the Card component.
 * This file serves as a visual reference and testing ground.
 */
const CardDemo: React.FC = () => {
  const [clickCount, setClickCount] = useState(0);

  return (
    <div className="p-8 bg-gray-50 min-h-screen" dir="rtl">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Card Component Demo
          </h1>
          <p className="text-gray-600">
            Flexible content container with shadow and padding variants
          </p>
        </div>

        {/* Shadow Variants */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Shadow Variants
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card shadow="none">
              <h3 className="text-lg font-semibold mb-2">ללא צל</h3>
              <p className="text-gray-600">shadow="none"</p>
            </Card>

            <Card shadow="sm">
              <h3 className="text-lg font-semibold mb-2">צל קטן</h3>
              <p className="text-gray-600">shadow="sm"</p>
              <p className="text-sm text-gray-500 mt-2">
                Level 1: Resting state
              </p>
            </Card>

            <Card shadow="md">
              <h3 className="text-lg font-semibold mb-2">צל בינוני</h3>
              <p className="text-gray-600">shadow="md" (default)</p>
              <p className="text-sm text-gray-500 mt-2">
                Level 2: Standard elevation
              </p>
            </Card>

            <Card shadow="lg">
              <h3 className="text-lg font-semibold mb-2">צל גדול</h3>
              <p className="text-gray-600">shadow="lg"</p>
              <p className="text-sm text-gray-500 mt-2">
                Level 3: Elevated state
              </p>
            </Card>
          </div>
        </section>

        {/* Padding Variants */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Padding Variants
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card padding="none" className="border-2 border-dashed border-gray-300">
              <div className="p-4 bg-blue-50">
                <h3 className="text-lg font-semibold mb-2">ללא ריווח</h3>
                <p className="text-gray-600">padding="none" (p-0)</p>
              </div>
            </Card>

            <Card padding="sm">
              <h3 className="text-lg font-semibold mb-2">ריווח קטן</h3>
              <p className="text-gray-600">padding="sm" (16px)</p>
            </Card>

            <Card padding="md">
              <h3 className="text-lg font-semibold mb-2">ריווח בינוני</h3>
              <p className="text-gray-600">padding="md" (24px)</p>
              <p className="text-sm text-gray-500 mt-2">Default</p>
            </Card>

            <Card padding="lg">
              <h3 className="text-lg font-semibold mb-2">ריווח גדול</h3>
              <p className="text-gray-600">padding="lg" (32px)</p>
            </Card>
          </div>
        </section>

        {/* Hoverable Cards */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Hoverable Cards
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card hoverable onClick={() => setClickCount(clickCount + 1)}>
              <h3 className="text-lg font-semibold mb-2">כרטיס אינטראקטיבי</h3>
              <p className="text-gray-600 mb-4">העבר עכבר ולחץ</p>
              <p className="text-sm text-primary font-medium">
                נלחצתי {clickCount} פעמים
              </p>
            </Card>

            <Card hoverable shadow="sm" onClick={() => alert('Clicked!')}>
              <h3 className="text-lg font-semibold mb-2">עם צל קטן</h3>
              <p className="text-gray-600">hoverable + shadow="sm"</p>
            </Card>

            <Card hoverable shadow="lg" onClick={() => alert('Clicked!')}>
              <h3 className="text-lg font-semibold mb-2">עם צל גדול</h3>
              <p className="text-gray-600">hoverable + shadow="lg"</p>
            </Card>
          </div>
        </section>

        {/* Image Cards */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Image Cards
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card padding="none" hoverable>
              <div className="aspect-video bg-gradient-to-br from-blue-400 to-blue-600" />
              <div className="p-4">
                <h3 className="text-lg font-semibold mb-2">כרטיס תמונה</h3>
                <p className="text-gray-600">padding="none" for images</p>
              </div>
            </Card>

            <Card padding="none" hoverable>
              <div className="aspect-video bg-gradient-to-br from-purple-400 to-purple-600" />
              <div className="p-4">
                <h3 className="text-lg font-semibold mb-2">תוכן מעורב</h3>
                <p className="text-gray-600">Image + padded content</p>
              </div>
            </Card>

            <Card padding="none" hoverable>
              <div className="aspect-video bg-gradient-to-br from-emerald-400 to-emerald-600" />
              <div className="p-4">
                <h3 className="text-lg font-semibold mb-2">פריסה גמישה</h3>
                <p className="text-gray-600">Flexible layout</p>
              </div>
            </Card>
          </div>
        </section>

        {/* Complex Content */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Complex Content Examples
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Feature Card */}
            <Card>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-primary/10 rounded-lg">
                  <svg
                    className="w-6 h-6 text-primary"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold mb-2">
                    עיבוד OCR מתקדם
                  </h3>
                  <p className="text-gray-600">
                    טכנולוגיית זיהוי תווים אוטומטית עם דיוק של 95%+ לקבלות בעברית
                  </p>
                </div>
              </div>
            </Card>

            {/* Stat Card */}
            <Card>
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-2">סך הוצאות החודש</p>
                <p className="text-4xl font-bold font-mono text-gray-900 mb-4">
                  ₪12,345.67
                </p>
                <div className="flex items-center justify-center gap-2 text-emerald-600">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                    />
                  </svg>
                  <span className="text-sm font-medium">+12.5%</span>
                  <span className="text-sm text-gray-500">לעומת חודש קודם</span>
                </div>
              </div>
            </Card>
          </div>
        </section>

        {/* Semantic HTML Variants */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Semantic HTML
          </h2>
          <div className="space-y-4">
            <Card as="article">
              <h3 className="text-lg font-semibold mb-2">Article Card</h3>
              <p className="text-gray-600">Rendered as &lt;article&gt;</p>
            </Card>

            <Card as="section">
              <h3 className="text-lg font-semibold mb-2">Section Card</h3>
              <p className="text-gray-600">Rendered as &lt;section&gt;</p>
            </Card>
          </div>
        </section>

        {/* Custom Styling */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Custom Styling
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="border-2 border-primary">
              <h3 className="text-lg font-semibold mb-2 text-primary">
                גבול מותאם
              </h3>
              <p className="text-gray-600">
                className="border-2 border-primary"
              </p>
            </Card>

            <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-none">
              <h3 className="text-lg font-semibold mb-2">רקע גרדיאנט</h3>
              <p className="text-gray-600">
                Custom gradient background
              </p>
            </Card>
          </div>
        </section>
      </div>
    </div>
  );
};

export default CardDemo;
