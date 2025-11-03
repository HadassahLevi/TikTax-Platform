import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Plus, TrendingUp, TrendingDown, Receipt, 
  Download, Calendar, DollarSign, FileText
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import PageContainer from '@/components/layout/PageContainer';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import { useReceipt, useLoadStatistics } from '@/hooks/useReceipt';
import { useAuth } from '@/hooks/useAuth';
import { formatAmount, formatDateIL, DEFAULT_CATEGORIES } from '@/types/receipt.types';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, remainingReceipts, usagePercentage } = useAuth();
  const { statistics, isLoadingStats, fetchStatistics } = useReceipt();
  
  useLoadStatistics();
  
  // Refresh statistics on mount
  useEffect(() => {
    fetchStatistics();
  }, []);
  
  if (isLoadingStats && !statistics) {
    return (
      <PageContainer title="לוח בקרה" loading={true}>
        <div />
      </PageContainer>
    );
  }
  
  if (!statistics) {
    return (
      <PageContainer title="לוח בקרה">
        <div className="text-center py-16">
          <p className="text-gray-600">לא ניתן לטעון נתונים</p>
        </div>
      </PageContainer>
    );
  }
  
  // Calculate month-over-month change
  const monthChange = statistics.lastMonth.amount > 0
    ? ((statistics.thisMonth.amount - statistics.lastMonth.amount) / statistics.lastMonth.amount) * 100
    : 0;
  
  // Prepare chart data
  const chartData = statistics.byCategory
    .slice(0, 5) // Top 5 categories
    .map(cat => ({
      name: cat.category.nameHe,
      value: cat.amount,
      color: cat.category.color
    }));
  
  // Usage warning level
  const usageLevel = usagePercentage();
  const showUsageWarning = usageLevel >= 80;
  
  return (
    <PageContainer
      title="לוח בקרה"
      subtitle={`שלום, ${user?.fullName || 'משתמש'}`}
      action={
        <Button
          variant="primary"
          onClick={() => navigate('/receipts/new')}
          icon={<Plus size={20} />}
        >
          הוסף קבלה
        </Button>
      }
    >
      <div className="space-y-6">
        
        {/* Usage warning banner */}
        {showUsageWarning && (
          <div className={`
            p-4 rounded-lg border flex items-start gap-3
            ${usageLevel >= 100 
              ? 'bg-red-50 border-red-200' 
              : 'bg-yellow-50 border-yellow-200'
            }
          `}>
            <FileText size={24} className={usageLevel >= 100 ? 'text-red-600' : 'text-yellow-600'} />
            <div className="flex-1">
              <p className="font-600 mb-1">
                {usageLevel >= 100 
                  ? 'הגעת למכסת הקבלות החודשית' 
                  : 'אתה מתקרב למכסת הקבלות'
                }
              </p>
              <p className="text-sm">
                {usageLevel >= 100
                  ? 'שדרג את התוכנית שלך כדי להמשיך להעלות קבלות'
                  : `נותרו לך ${remainingReceipts()} קבלות החודש`
                }
              </p>
            </div>
            <Button
              variant={usageLevel >= 100 ? 'danger' : 'secondary'}
              size="sm"
              onClick={() => navigate('/profile#subscription')}
            >
              שדרג תוכנית
            </Button>
          </div>
        )}
        
        {/* Quick stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card shadow="md" padding="lg">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center">
                <DollarSign size={24} className="text-primary-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">הוצאות החודש</p>
                <p className="text-2xl font-700 text-gray-900">
                  {formatAmount(statistics.thisMonth.amount)}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              {monthChange >= 0 ? (
                <TrendingUp size={16} className="text-red-600" />
              ) : (
                <TrendingDown size={16} className="text-green-600" />
              )}
              <span className={monthChange >= 0 ? 'text-red-600' : 'text-green-600'}>
                {Math.abs(monthChange).toFixed(1)}%
              </span>
              <span className="text-gray-600">לעומת חודש שעבר</span>
            </div>
          </Card>
          
          <Card shadow="md" padding="lg">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
                <Receipt size={24} className="text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">קבלות החודש</p>
                <p className="text-2xl font-700 text-gray-900">
                  {statistics.thisMonth.count}
                </p>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              ממוצע: {formatAmount(statistics.thisMonth.count > 0 
                ? statistics.thisMonth.amount / statistics.thisMonth.count 
                : 0
              )}
            </p>
          </Card>
          
          <Card shadow="md" padding="lg">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
                <FileText size={24} className="text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">סך כל הקבלות</p>
                <p className="text-2xl font-700 text-gray-900">
                  {statistics.totalReceipts}
                </p>
              </div>
            </div>
            <p className="text-sm text-gray-600">
              {formatAmount(statistics.totalAmount)} סך הכל
            </p>
          </Card>
          
          <Card shadow="md" padding="lg">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
                <Calendar size={24} className="text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">קבלות שנותרו</p>
                <p className="text-2xl font-700 text-gray-900">
                  {remainingReceipts()}
                </p>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full transition-all"
                style={{ width: `${Math.min(usageLevel, 100)}%` }}
              />
            </div>
          </Card>
        </div>
        
        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Top Categories Chart */}
          <Card shadow="md" padding="lg">
            <h2 className="text-xl font-600 text-gray-900 mb-6">
              קטגוריות מובילות
            </h2>
            
            {chartData.length > 0 ? (
              <>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={chartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={(entry) => `${entry.name}: ${((entry.value / statistics.thisMonth.amount) * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value: number) => formatAmount(value)}
                    />
                  </PieChart>
                </ResponsiveContainer>
                
                {/* Category legend */}
                <div className="mt-6 space-y-2">
                  {statistics.byCategory.slice(0, 5).map(cat => (
                    <div key={cat.categoryId} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: cat.category.color }}
                        />
                        <span className="text-sm text-gray-700">{cat.category.nameHe}</span>
                      </div>
                      <div className="text-left">
                        <p className="text-sm font-600 text-gray-900">
                          {formatAmount(cat.amount)}
                        </p>
                        <p className="text-xs text-gray-500">
                          {cat.count} קבלות
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                  <FileText size={32} className="text-gray-400" />
                </div>
                <p className="text-gray-600">אין עדיין קבלות</p>
                <p className="text-sm text-gray-500 mt-1">התחל להעלות קבלות לראות סטטיסטיקות</p>
              </div>
            )}
          </Card>
          
          {/* Recent Receipts */}
          <Card shadow="md" padding="lg">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-600 text-gray-900">
                קבלות אחרונות
              </h2>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/archive')}
              >
                הצג הכל
              </Button>
            </div>
            
            {statistics.recentReceipts.length > 0 ? (
              <div className="space-y-3">
                {statistics.recentReceipts.slice(0, 5).map(receipt => {
                  const category = DEFAULT_CATEGORIES.find(c => c.id === receipt.categoryId);
                  return (
                    <div
                      key={receipt.id}
                      onClick={() => navigate(`/receipts/${receipt.id}`)}
                      className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                    >
                      {/* Thumbnail */}
                      <div className="w-16 h-16 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
                        <img
                          src={receipt.imageUrl}
                          alt={receipt.vendorName}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      
                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-1">
                          <p className="font-600 text-gray-900 truncate">
                            {receipt.vendorName}
                          </p>
                          <p className="font-700 text-gray-900 flex-shrink-0 ml-3">
                            {formatAmount(receipt.totalAmount)}
                          </p>
                        </div>
                        <div className="flex items-center gap-2 text-xs text-gray-600">
                          <span>{formatDateIL(receipt.date)}</span>
                          {category && (
                            <>
                              <span>•</span>
                              <span style={{ color: category.color }}>
                                {category.nameHe}
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
                  <Receipt size={32} className="text-gray-400" />
                </div>
                <p className="text-gray-600">אין עדיין קבלות</p>
                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => navigate('/receipts/new')}
                  icon={<Plus size={18} />}
                  className="mt-4"
                >
                  הוסף קבלה ראשונה
                </Button>
              </div>
            )}
          </Card>
        </div>
        
        {/* Quick actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card
            shadow="sm"
            padding="lg"
            hoverable
            onClick={() => navigate('/receipts/new')}
            className="cursor-pointer border-2 border-dashed border-primary-300 hover:border-primary-500 transition-colors"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center mb-3">
                <Plus size={32} className="text-primary-600" />
              </div>
              <h3 className="font-600 text-gray-900 mb-1">הוסף קבלה חדשה</h3>
              <p className="text-sm text-gray-600">צלם או העלה קבלה</p>
            </div>
          </Card>
          
          <Card
            shadow="sm"
            padding="lg"
            hoverable
            onClick={() => navigate('/export')}
            className="cursor-pointer"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-3">
                <Download size={32} className="text-green-600" />
              </div>
              <h3 className="font-600 text-gray-900 mb-1">ייצוא לאקסל</h3>
              <p className="text-sm text-gray-600">הורד דוח לרו"ח</p>
            </div>
          </Card>
          
          <Card
            shadow="sm"
            padding="lg"
            hoverable
            onClick={() => navigate('/archive')}
            className="cursor-pointer"
          >
            <div className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-3">
                <FileText size={32} className="text-blue-600" />
              </div>
              <h3 className="font-600 text-gray-900 mb-1">צפה בארכיון</h3>
              <p className="text-sm text-gray-600">כל הקבלות שלך</p>
            </div>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
};

export default DashboardPage;
