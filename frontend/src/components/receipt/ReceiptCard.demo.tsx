import React, { useState } from 'react';
import ReceiptCard from './ReceiptCard';
import type { Receipt } from '@/types';

/**
 * ReceiptCard Component Demo
 * 
 * Demonstrates all states and usage patterns for the ReceiptCard component.
 */
const ReceiptCardDemo: React.FC = () => {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // Mock receipt data
  const mockReceipts: Receipt[] = [
    {
      id: '1',
      userId: 'user-1',
      businessName: 'סופר פארם',
      amount: 234.50,
      currency: 'ILS',
      date: '2024-11-01T10:30:00Z',
      category: 'office-supplies',
      status: 'completed',
      imageUrl: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300',
      ocrData: {
        businessName: 'סופר פארם',
        amount: 234.50,
        date: '2024-11-01',
        confidence: 0.95,
        rawText: '',
      },
      verified: true,
      createdAt: '2024-11-01T10:30:00Z',
      updatedAt: '2024-11-01T10:35:00Z',
    },
    {
      id: '2',
      userId: 'user-1',
      businessName: 'דלק - תחנת דלק רמת גן',
      amount: 450.00,
      currency: 'ILS',
      date: '2024-10-30T14:20:00Z',
      category: 'fuel',
      status: 'completed',
      imageUrl: 'https://images.unsplash.com/photo-1545685880-0b4c2456f6ba?w=400&h=300',
      ocrData: {
        businessName: 'דלק',
        amount: 450.00,
        date: '2024-10-30',
        confidence: 0.92,
        rawText: '',
      },
      verified: true,
      createdAt: '2024-10-30T14:20:00Z',
      updatedAt: '2024-10-30T14:25:00Z',
    },
    {
      id: '3',
      userId: 'user-1',
      businessName: 'קפה ג\'ו - רוטשילד',
      amount: 67.50,
      currency: 'ILS',
      date: '2024-10-29T09:15:00Z',
      category: 'meals',
      status: 'processing',
      imageUrl: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300',
      ocrData: {
        businessName: 'קפה ג\'ו',
        amount: 67.50,
        date: '2024-10-29',
        confidence: 0.88,
        rawText: '',
      },
      verified: false,
      createdAt: '2024-10-29T09:15:00Z',
      updatedAt: '2024-10-29T09:20:00Z',
    },
    {
      id: '4',
      userId: 'user-1',
      businessName: 'חשמל - חברת חשמל',
      amount: 892.30,
      currency: 'ILS',
      date: '2024-10-28T00:00:00Z',
      category: 'utilities',
      status: 'pending',
      imageUrl: 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=400&h=300',
      ocrData: {
        amount: 892.30,
        confidence: 0.75,
        rawText: '',
      },
      verified: false,
      createdAt: '2024-10-28T16:00:00Z',
      updatedAt: '2024-10-28T16:00:00Z',
    },
    {
      id: '5',
      userId: 'user-1',
      businessName: 'משרד ושות\' - שירותים משפטיים',
      amount: 3500.00,
      currency: 'ILS',
      date: '2024-10-25T13:00:00Z',
      category: 'professional-services',
      status: 'completed',
      imageUrl: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=300',
      ocrData: {
        businessName: 'משרד ושות\'',
        amount: 3500.00,
        date: '2024-10-25',
        confidence: 0.91,
        rawText: '',
      },
      verified: true,
      createdAt: '2024-10-25T13:00:00Z',
      updatedAt: '2024-10-25T13:10:00Z',
    },
    {
      id: '6',
      userId: 'user-1',
      businessName: 'מסעדת לה סקאלה',
      amount: 420.00,
      currency: 'ILS',
      date: '2024-10-24T19:30:00Z',
      category: 'meals',
      status: 'failed',
      imageUrl: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300',
      ocrData: {
        confidence: 0.45,
        rawText: 'Low quality image',
      },
      verified: false,
      createdAt: '2024-10-24T19:30:00Z',
      updatedAt: '2024-10-24T19:35:00Z',
    },
  ];

  return (
    <div className="p-8 bg-gray-50 min-h-screen" dir="rtl">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            ReceiptCard Component Demo
          </h1>
          <p className="text-gray-600">
            Archive grid cards with image thumbnails, status, and category badges
          </p>
        </div>

        {/* All Receipts Grid */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            All Receipt States
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockReceipts.map((receipt) => (
              <ReceiptCard
                key={receipt.id}
                receipt={receipt}
                selected={selectedId === receipt.id}
                onClick={(r) => setSelectedId(r.id)}
              />
            ))}
          </div>
          {selectedId && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-900">
                <strong>Selected Receipt ID:</strong> {selectedId}
                <button
                  onClick={() => setSelectedId(null)}
                  className="mr-4 text-blue-600 hover:text-blue-800 underline"
                >
                  נקה בחירה
                </button>
              </p>
            </div>
          )}
        </section>

        {/* Status Breakdown */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            By Status
          </h2>
          
          <div className="space-y-8">
            {/* Completed */}
            <div>
              <h3 className="text-lg font-medium mb-4 text-emerald-600">
                ✓ Completed (הושלם)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockReceipts
                  .filter((r) => r.status === 'completed')
                  .map((receipt) => (
                    <ReceiptCard
                      key={receipt.id}
                      receipt={receipt}
                      onClick={(r) => console.log('View', r.id)}
                    />
                  ))}
              </div>
            </div>

            {/* Processing */}
            <div>
              <h3 className="text-lg font-medium mb-4 text-blue-600">
                ⏱ Processing (בעיבוד)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockReceipts
                  .filter((r) => r.status === 'processing')
                  .map((receipt) => (
                    <ReceiptCard
                      key={receipt.id}
                      receipt={receipt}
                      onClick={(r) => console.log('View', r.id)}
                    />
                  ))}
              </div>
            </div>

            {/* Pending */}
            <div>
              <h3 className="text-lg font-medium mb-4 text-yellow-600">
                ⏳ Pending (ממתין)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockReceipts
                  .filter((r) => r.status === 'pending')
                  .map((receipt) => (
                    <ReceiptCard
                      key={receipt.id}
                      receipt={receipt}
                      onClick={(r) => console.log('View', r.id)}
                    />
                  ))}
              </div>
            </div>

            {/* Failed */}
            <div>
              <h3 className="text-lg font-medium mb-4 text-red-600">
                ✗ Failed (נכשל)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockReceipts
                  .filter((r) => r.status === 'failed')
                  .map((receipt) => (
                    <ReceiptCard
                      key={receipt.id}
                      receipt={receipt}
                      onClick={(r) => console.log('Retry', r.id)}
                    />
                  ))}
              </div>
            </div>
          </div>
        </section>

        {/* Responsive Layouts */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Responsive Layouts
          </h2>

          {/* Single Column (Mobile) */}
          <div className="mb-8">
            <h3 className="text-lg font-medium mb-4 text-gray-700">
              Single Column (Mobile)
            </h3>
            <div className="grid grid-cols-1 gap-4">
              {mockReceipts.slice(0, 2).map((receipt) => (
                <ReceiptCard key={receipt.id} receipt={receipt} />
              ))}
            </div>
          </div>

          {/* Two Columns (Tablet) */}
          <div className="mb-8">
            <h3 className="text-lg font-medium mb-4 text-gray-700">
              Two Columns (Tablet)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {mockReceipts.slice(0, 4).map((receipt) => (
                <ReceiptCard key={receipt.id} receipt={receipt} />
              ))}
            </div>
          </div>

          {/* Four Columns (Desktop) */}
          <div>
            <h3 className="text-lg font-medium mb-4 text-gray-700">
              Four Columns (Large Desktop)
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {mockReceipts.map((receipt) => (
                <ReceiptCard key={receipt.id} receipt={receipt} />
              ))}
            </div>
          </div>
        </section>

        {/* Feature Highlights */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Feature Highlights
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Verified Badge */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-700">
                ✓ Verified Badge
              </h3>
              <ReceiptCard receipt={mockReceipts[0]} />
              <p className="text-sm text-gray-600">
                Green verified badge appears when receipt.verified === true
              </p>
            </div>

            {/* Low Confidence Warning */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-700">
                ⚠ Low Confidence Warning
              </h3>
              <ReceiptCard receipt={mockReceipts[3]} />
              <p className="text-sm text-gray-600">
                Amber alert shown when OCR confidence {'<'} 80%
              </p>
            </div>
          </div>
        </section>

        {/* Archive Page Simulation */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Complete Archive Page Example
          </h2>
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6 pb-4 border-b">
              <h3 className="text-xl font-semibold">ארכיון קבלות</h3>
              <div className="text-sm text-gray-600">
                {mockReceipts.length} קבלות
              </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {mockReceipts.map((receipt) => (
                <ReceiptCard
                  key={receipt.id}
                  receipt={receipt}
                  selected={selectedId === receipt.id}
                  onClick={(r) => {
                    setSelectedId(r.id);
                    console.log('Opening receipt detail modal for:', r.id);
                  }}
                />
              ))}
            </div>

            {/* Pagination Placeholder */}
            <div className="mt-6 pt-4 border-t flex justify-center">
              <div className="text-sm text-gray-500">
                עמוד 1 מתוך 1
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ReceiptCardDemo;
