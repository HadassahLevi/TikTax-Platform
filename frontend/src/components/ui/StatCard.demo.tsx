import React from 'react';
import {
  Receipt,
  TrendingUp,
  Users,
  DollarSign,
  ShoppingCart,
  Calendar,
  FileText,
  AlertCircle,
} from 'lucide-react';
import StatCard from './StatCard';

/**
 * StatCard Component Demo
 * 
 * Demonstrates all variants and usage patterns for the StatCard component.
 */
const StatCardDemo: React.FC = () => {
  return (
    <div className="p-8 bg-gray-50 min-h-screen" dir="rtl">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            StatCard Component Demo
          </h1>
          <p className="text-gray-600">
            Dashboard statistics cards with icons, changes, and gradients
          </p>
        </div>

        {/* Basic Stats */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Basic Statistics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              label="סך הוצאות החודש"
              value="₪12,345.67"
            />

            <StatCard
              label="קבלות החודש"
              value={42}
            />

            <StatCard
              label="ממוצע לקבלה"
              value="₪294.18"
            />

            <StatCard
              label="קטגוריות פעילות"
              value={8}
            />
          </div>
        </section>

        {/* With Icons */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            With Icons
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              label="סך הוצאות"
              value="₪45,678.90"
              icon={DollarSign}
              iconColor="text-emerald-500"
            />

            <StatCard
              label="קבלות"
              value={156}
              icon={Receipt}
              iconColor="text-blue-500"
            />

            <StatCard
              label="ספקים"
              value={23}
              icon={ShoppingCart}
              iconColor="text-purple-500"
            />

            <StatCard
              label="חודשים"
              value={12}
              icon={Calendar}
              iconColor="text-amber-500"
            />
          </div>
        </section>

        {/* With Percentage Changes */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            With Percentage Changes
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              label="הוצאות החודש"
              value="₪8,500.00"
              icon={TrendingUp}
              iconColor="text-blue-500"
              change={12.5}
              changeLabel="לעומת חודש קודם"
            />

            <StatCard
              label="קבלות חדשות"
              value={28}
              icon={Receipt}
              iconColor="text-emerald-500"
              change={8.3}
              changeLabel="השבוע"
            />

            <StatCard
              label="ממתינים לעיבוד"
              value={5}
              icon={FileText}
              iconColor="text-amber-500"
              change={-40}
              changeLabel="לעומת שבוע שעבר"
            />

            <StatCard
              label="ממוצע יומי"
              value="₪283.33"
              icon={Calendar}
              iconColor="text-purple-500"
              change={-5.2}
              changeLabel="החודש"
            />
          </div>
        </section>

        {/* Gradient Backgrounds */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Gradient Backgrounds
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              label="יתרה כוללת"
              value="₪98,765.43"
              icon={DollarSign}
              gradient
              gradientColors={{ from: 'from-blue-500', to: 'to-blue-700' }}
              change={15.7}
              changeLabel="גידול חודשי"
            />

            <StatCard
              label="הכנסות החודש"
              value="₪125,000"
              icon={TrendingUp}
              gradient
              gradientColors={{ from: 'from-emerald-500', to: 'to-emerald-700' }}
              change={23.8}
              changeLabel="לעומת חודש קודם"
            />

            <StatCard
              label="לקוחות פעילים"
              value={342}
              icon={Users}
              gradient
              gradientColors={{ from: 'from-purple-500', to: 'to-purple-700' }}
              change={18.2}
              changeLabel="צמיחה רבעונית"
            />

            <StatCard
              label="דוחות השלמו"
              value="92%"
              icon={FileText}
              gradient
              gradientColors={{ from: 'from-amber-500', to: 'to-amber-700' }}
              change={5.4}
              changeLabel="שיפור"
            />
          </div>
        </section>

        {/* Clickable Stats */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Clickable (Interactive)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <StatCard
              label="דורש תשומת לב"
              value={7}
              icon={AlertCircle}
              iconColor="text-red-500"
              onClick={() => alert('Navigate to pending receipts')}
            />

            <StatCard
              label="הושלמו היום"
              value={15}
              icon={Receipt}
              iconColor="text-emerald-500"
              change={25}
              onClick={() => alert('View completed receipts')}
            />

            <StatCard
              label="המתנה לאישור"
              value={3}
              icon={FileText}
              iconColor="text-amber-500"
              onClick={() => alert('Navigate to approvals')}
            />
          </div>
        </section>

        {/* Dashboard Layout Example */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Complete Dashboard Example
          </h2>
          
          {/* Top Row - Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <StatCard
              label="סך הוצאות חודש זה"
              value="₪12,345.67"
              icon={DollarSign}
              iconColor="text-blue-500"
              change={8.3}
              changeLabel="לעומת חודש שעבר"
            />

            <StatCard
              label="קבלות חודש זה"
              value={42}
              icon={Receipt}
              iconColor="text-emerald-500"
              change={15.2}
              changeLabel="לעומת חודש שעבר"
            />

            <StatCard
              label="ממוצע לקבלה"
              value="₪294.18"
              icon={TrendingUp}
              iconColor="text-purple-500"
              change={-5.8}
              changeLabel="לעומת חודש שעבר"
            />

            <StatCard
              label="קטגוריות פעילות"
              value={8}
              icon={ShoppingCart}
              iconColor="text-amber-500"
            />
          </div>

          {/* Bottom Row - Alerts */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard
              label="ממתינים לעיבוד"
              value={5}
              icon={FileText}
              iconColor="text-amber-500"
              onClick={() => alert('View pending')}
            />

            <StatCard
              label="דורש אימות"
              value={2}
              icon={AlertCircle}
              iconColor="text-red-500"
              onClick={() => alert('View verification needed')}
            />

            <StatCard
              label="הושלמו השבוע"
              value={38}
              icon={Receipt}
              iconColor="text-emerald-500"
              change={12}
              changeLabel="לעומת שבוע שעבר"
            />
          </div>
        </section>

        {/* Compact Layout */}
        <section>
          <h2 className="text-2xl font-semibold mb-6 text-gray-900">
            Compact 6-Column Layout
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <StatCard label="ינואר" value="₪8,234" />
            <StatCard label="פברואר" value="₪9,123" />
            <StatCard label="מרץ" value="₪7,891" />
            <StatCard label="אפריל" value="₪10,456" />
            <StatCard label="מאי" value="₪11,234" />
            <StatCard label="יוני" value="₪12,345" />
          </div>
        </section>
      </div>
    </div>
  );
};

export default StatCardDemo;
