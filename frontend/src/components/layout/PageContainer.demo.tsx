/**
 * PageContainer Component - Demo & Examples
 * 
 * This file demonstrates all usage patterns and variants of the PageContainer component.
 * Use this as a reference when implementing pages in the application.
 */

import React, { useState } from 'react';
import { 
  PageContainer, 
  GridSkeleton, 
  ListSkeleton, 
  StatsSkeleton,
  FormSkeleton 
} from './PageContainer';
import Button from '../ui/Button';
import Card from '../ui/Card';
import Input from '../ui/Input';
import { Search, Plus, Download, Filter } from 'lucide-react';

/**
 * Demo 1: Basic Dashboard Page
 */
export const BasicDashboardDemo: React.FC = () => {
  return (
    <PageContainer title="לוח בקרה" maxWidth="xl">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card padding="lg">
          <h3 className="text-lg font-semibold mb-2">הכנסות החודש</h3>
          <p className="text-3xl font-bold text-green-600">₪12,450</p>
        </Card>
        <Card padding="lg">
          <h3 className="text-lg font-semibold mb-2">הוצאות החודש</h3>
          <p className="text-3xl font-bold text-red-600">₪8,320</p>
        </Card>
        <Card padding="lg">
          <h3 className="text-lg font-semibold mb-2">יתרה</h3>
          <p className="text-3xl font-bold text-blue-600">₪4,130</p>
        </Card>
      </div>
    </PageContainer>
  );
};

/**
 * Demo 2: Archive Page with Search Action
 */
export const ArchiveWithSearchDemo: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <PageContainer
      title="ארכיון קבלות"
      subtitle="כל הקבלות שלך במקום אחד"
      action={
        <div className="flex gap-3">
          <div className="relative w-64">
            <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
            <Input
              type="text"
              placeholder="חיפוש..."
              value={searchQuery}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
              className="pr-10"
            />
          </div>
          <Button variant="secondary" icon={<Filter className="w-4 h-4" />}>
            סינון
          </Button>
        </div>
      }
      maxWidth="lg"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <Card key={i} hoverable padding="md">
            <p className="font-medium">קבלה #{i}</p>
            <p className="text-sm text-gray-600 mt-1">₪{(Math.random() * 1000).toFixed(2)}</p>
          </Card>
        ))}
      </div>
    </PageContainer>
  );
};

/**
 * Demo 3: Page with Loading State
 */
export const LoadingStateDemo: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);

  // Simulate data loading
  React.useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer
      title="טוען נתונים"
      subtitle="אנא המתן..."
      loading={isLoading}
      maxWidth="md"
    >
      <div className="space-y-4">
        <Card padding="lg">
          <h3 className="text-lg font-semibold">התוכן נטען...</h3>
          <p className="text-gray-600 mt-2">
            זה הטקסט שיופיע לאחר שהטעינה תסתיים
          </p>
        </Card>
      </div>
    </PageContainer>
  );
};

/**
 * Demo 4: Multiple Actions in Header
 */
export const MultipleActionsDemo: React.FC = () => {
  return (
    <PageContainer
      title="ניהול קבלות"
      action={
        <>
          <Button variant="secondary" icon={<Download className="w-4 h-4" />}>
            ייצוא
          </Button>
          <Button variant="primary" icon={<Plus className="w-4 h-4" />}>
            הוסף קבלה
          </Button>
        </>
      }
      maxWidth="lg"
    >
      <Card>
        <p>תוכן הדף</p>
      </Card>
    </PageContainer>
  );
};

/**
 * Demo 5: Full Width Layout (No Padding)
 */
export const FullWidthDemo: React.FC = () => {
  return (
    <PageContainer maxWidth="full" noPadding>
      <div className="h-96 bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white">
        <h2 className="text-4xl font-bold">פריסה מלאה ללא ריווח</h2>
      </div>
    </PageContainer>
  );
};

/**
 * Demo 6: Simple Page (No Title/Actions)
 */
export const SimplePageDemo: React.FC = () => {
  return (
    <PageContainer maxWidth="sm">
      <Card padding="lg">
        <h2 className="text-2xl font-bold mb-4">דף פשוט</h2>
        <p className="text-gray-600">
          לפעמים אתה רק צריך container פשוט עם ריווח וללא header
        </p>
      </Card>
    </PageContainer>
  );
};

/**
 * Demo 7: Form Page with Skeleton
 */
export const FormPageDemo: React.FC = () => {
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer
      title="הגדרות פרופיל"
      subtitle="עדכן את פרטיך האישיים"
      maxWidth="md"
      loading={loading}
    >
      {loading ? (
        <FormSkeleton />
      ) : (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">שם מלא</label>
            <Input type="text" placeholder="הכנס שם מלא" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">אימייל</label>
            <Input type="email" placeholder="your@email.com" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">טלפון</label>
            <Input type="tel" placeholder="050-1234567" />
          </div>
          <div className="flex gap-3 pt-4">
            <Button variant="primary">שמור שינויים</Button>
            <Button variant="secondary">ביטול</Button>
          </div>
        </div>
      )}
    </PageContainer>
  );
};

/**
 * Demo 8: Grid Layout with Custom Skeleton
 */
export const GridLayoutDemo: React.FC = () => {
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer
      title="גלריית קבלות"
      maxWidth="xl"
    >
      {loading ? (
        <GridSkeleton count={9} />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 9 }).map((_, i) => (
            <Card key={i} hoverable padding="md">
              <div className="aspect-square bg-gray-100 rounded-lg mb-3" />
              <h3 className="font-medium">קבלה #{i + 1}</h3>
              <p className="text-sm text-gray-600">₪{(Math.random() * 1000).toFixed(2)}</p>
            </Card>
          ))}
        </div>
      )}
    </PageContainer>
  );
};

/**
 * Demo 9: Stats Dashboard with Skeleton
 */
export const StatsDashboardDemo: React.FC = () => {
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1800);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer
      title="סטטיסטיקות"
      subtitle="נתוני העסק שלך"
      maxWidth="xl"
    >
      {loading ? (
        <StatsSkeleton />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { label: 'סה"כ קבלות', value: '1,234', change: '+12%' },
            { label: 'הכנסות', value: '₪45,678', change: '+8%' },
            { label: 'הוצאות', value: '₪23,456', change: '-3%' },
            { label: 'יתרה', value: '₪22,222', change: '+15%' },
          ].map((stat, i) => (
            <Card key={i} padding="lg">
              <p className="text-sm text-gray-600 mb-2">{stat.label}</p>
              <p className="text-2xl font-bold mb-1">{stat.value}</p>
              <p className={`text-sm ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change}
              </p>
            </Card>
          ))}
        </div>
      )}
    </PageContainer>
  );
};

/**
 * Demo 10: List Layout with Skeleton
 */
export const ListLayoutDemo: React.FC = () => {
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1600);
    return () => clearTimeout(timer);
  }, []);

  return (
    <PageContainer
      title="רשימת עסקאות"
      maxWidth="md"
    >
      {loading ? (
        <ListSkeleton count={8} />
      ) : (
        <div className="space-y-3">
          {Array.from({ length: 8 }).map((_, i) => (
            <Card key={i} padding="md" hoverable>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium">עסקה #{i + 1}</h3>
                  <p className="text-sm text-gray-600">
                    {new Date().toLocaleDateString('he-IL')}
                  </p>
                </div>
                <p className="text-lg font-semibold">
                  ₪{(Math.random() * 500).toFixed(2)}
                </p>
              </div>
            </Card>
          ))}
        </div>
      )}
    </PageContainer>
  );
};

/**
 * All Demos Combined (for testing)
 */
export const AllPageContainerDemos: React.FC = () => {
  const [activeDemo, setActiveDemo] = useState(0);

  const demos = [
    { name: 'Basic Dashboard', component: <BasicDashboardDemo /> },
    { name: 'Archive with Search', component: <ArchiveWithSearchDemo /> },
    { name: 'Loading State', component: <LoadingStateDemo /> },
    { name: 'Multiple Actions', component: <MultipleActionsDemo /> },
    { name: 'Full Width', component: <FullWidthDemo /> },
    { name: 'Simple Page', component: <SimplePageDemo /> },
    { name: 'Form Page', component: <FormPageDemo /> },
    { name: 'Grid Layout', component: <GridLayoutDemo /> },
    { name: 'Stats Dashboard', component: <StatsDashboardDemo /> },
    { name: 'List Layout', component: <ListLayoutDemo /> },
  ];

  return (
    <div>
      <div className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 p-4 z-50">
        <div className="flex gap-2 overflow-x-auto">
          {demos.map((demo, i) => (
            <Button
              key={i}
              variant={activeDemo === i ? 'primary' : 'secondary'}
              size="sm"
              onClick={() => setActiveDemo(i)}
            >
              {demo.name}
            </Button>
          ))}
        </div>
      </div>
      <div className="pt-20">
        {demos[activeDemo].component}
      </div>
    </div>
  );
};

export default AllPageContainerDemos;
