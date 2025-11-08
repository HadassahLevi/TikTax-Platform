import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Search,
  Filter,
  SortAsc,
  Grid,
  List,
  Calendar,
  DollarSign,
  Tag,
  X,
  Download,
  Plus,
  Receipt as ReceiptIcon
} from 'lucide-react';
import { PageContainer } from '@/components/layout/PageContainer';
import { EmptyState } from '@/components/EmptyState';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Card from '@/components/ui/Card';
import Modal from '@/components/ui/Modal';
import {
  useReceipt,
  useLoadReceipts,
  useInfiniteScroll,
  useReceiptFilters
} from '@/hooks/useReceipt';
import {
  formatAmount,
  formatDateIL,
  DEFAULT_CATEGORIES
} from '@/types/receipt.types';
import type {
  ReceiptSortField,
  ReceiptSortOrder
} from '@/types/receipt.types';
import { SkeletonCard, SkeletonList, LoadingSpinner } from '@/components/loading';
import { useMinimumLoading } from '@/hooks/useMinimumLoading';

/**
 * Archive Page Component
 * 
 * Main receipt archive with:
 * - Search with debounce
 * - Advanced filters (date, category, amount)
 * - Sorting options
 * - Grid/List view toggle
 * - Infinite scroll pagination
 * - Stats summary
 * 
 * @component
 */
export const ArchivePage: React.FC = () => {
  const navigate = useNavigate();
  const {
    receipts,
    total,
    isLoadingList,
    searchReceipts,
    loadMoreReceipts,
    setSort,
    clearFilters
  } = useReceipt();

  const { filters, updateFilter, hasActiveFilters } = useReceiptFilters();

  useLoadReceipts();

  // UI State
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [showSortModal, setShowSortModal] = useState(false);

  // Sort state
  const [sortField, setSortField] = useState<ReceiptSortField>('date');
  const [sortOrder, setSortOrder] = useState<ReceiptSortOrder>('desc');

  // Filter state
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [amountRange, setAmountRange] = useState({ min: '', max: '' });

  // Infinite scroll
  useInfiniteScroll(loadMoreReceipts);

  // Use minimum loading time to prevent flash
  const initialLoading = useMinimumLoading(isLoadingList && receipts.length === 0, 300);
  const loadingMore = isLoadingList && receipts.length > 0;

  // Debounced search
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery.length >= 2 || searchQuery.length === 0) {
        searchReceipts(searchQuery);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [searchQuery, searchReceipts]);

  // Apply sort
  const handleSort = (field: ReceiptSortField, order: ReceiptSortOrder) => {
    setSortField(field);
    setSortOrder(order);
    setSort({ field, order });
    setShowSortModal(false);
  };

  // Apply filters
  const applyFilters = () => {
    updateFilter('startDate', dateRange.start || undefined);
    updateFilter('endDate', dateRange.end || undefined);
    updateFilter(
      'categoryIds',
      selectedCategories.length > 0 ? selectedCategories : undefined
    );
    updateFilter(
      'minAmount',
      amountRange.min ? parseFloat(amountRange.min) : undefined
    );
    updateFilter(
      'maxAmount',
      amountRange.max ? parseFloat(amountRange.max) : undefined
    );
    setShowFilterModal(false);
  };

  // Clear all filters
  const handleClearFilters = () => {
    setDateRange({ start: '', end: '' });
    setSelectedCategories([]);
    setAmountRange({ min: '', max: '' });
    clearFilters();
    setShowFilterModal(false);
  };

  // Calculate stats
  const totalAmount = receipts.reduce((sum, r) => sum + r.totalAmount, 0);
  const thisMonthReceipts = receipts.filter((r) => {
    const receiptDate = new Date(r.date);
    const now = new Date();
    return (
      receiptDate.getMonth() === now.getMonth() &&
      receiptDate.getFullYear() === now.getFullYear()
    );
  });

  // Initial loading state
  if (initialLoading) {
    return (
      <PageContainer title="ארכיון קבלות">
        {/* Stats bar skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <SkeletonCard variant="stat" />
          <SkeletonCard variant="stat" />
          <SkeletonCard variant="stat" />
        </div>

        {/* Search/Filter Bar Skeleton */}
        <div className="mb-6 space-y-4 animate-pulse">
          <div className="h-12 bg-gray-200 rounded-lg"></div>
          <div className="flex gap-2">
            <div className="h-10 bg-gray-200 rounded w-24"></div>
            <div className="h-10 bg-gray-200 rounded w-24"></div>
            <div className="h-10 bg-gray-200 rounded w-24"></div>
          </div>
        </div>

        {/* Receipts Grid Skeleton */}
        <SkeletonList 
          count={12} 
          variant="receipt" 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        />
      </PageContainer>
    );
  }

  return (
    <PageContainer
      title="ארכיון קבלות"
      subtitle={`סך הכל ${total} קבלות`}
      loading={isLoadingList && receipts.length === 0}
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
      {/* Stats bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card shadow="sm" padding="md">
          <p className="text-sm text-gray-600 mb-1">סך כל ההוצאות</p>
          <p className="text-2xl font-700 text-gray-900">
            {formatAmount(totalAmount)}
          </p>
        </Card>

        <Card shadow="sm" padding="md">
          <p className="text-sm text-gray-600 mb-1">קבלות החודש</p>
          <p className="text-2xl font-700 text-gray-900">
            {thisMonthReceipts.length}
          </p>
        </Card>

        <Card shadow="sm" padding="md">
          <p className="text-sm text-gray-600 mb-1">ממוצע לקבלה</p>
          <p className="text-2xl font-700 text-gray-900">
            {receipts.length > 0
              ? formatAmount(totalAmount / receipts.length)
              : '₪0.00'}
          </p>
        </Card>
      </div>

      {/* Search and filters bar */}
      <div className="flex flex-col md:flex-row gap-3 mb-6">
        <div className="flex-1">
          <Input
            data-search-input
            type="search"
            placeholder="חפש לפי שם עסק, מספר קבלה..."
            value={searchQuery}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
            icon={<Search size={20} />}
            aria-label="חיפוש קבלות"
          />
        </div>

        <div className="flex gap-2">
          <Button
            variant={hasActiveFilters() ? 'primary' : 'secondary'}
            onClick={() => setShowFilterModal(true)}
            icon={<Filter size={20} />}
          >
            סינון
            {hasActiveFilters() && (
              <span className="mr-2 px-2 py-0.5 bg-white rounded-full text-xs">
                {Object.keys(filters).length}
              </span>
            )}
          </Button>

          <Button
            variant="secondary"
            onClick={() => setShowSortModal(true)}
            icon={<SortAsc size={20} />}
          >
            מיון
          </Button>

          <Button
            variant="secondary"
            onClick={() => navigate('/export')}
            icon={<Download size={20} />}
          >
            ייצוא
          </Button>

          {/* View toggle */}
          <div className="hidden md:flex border border-gray-300 rounded-lg overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 ${
                viewMode === 'grid'
                  ? 'bg-primary-50 text-primary-600'
                  : 'bg-white text-gray-600'
              } transition-colors`}
              aria-label="תצוגת רשת"
            >
              <Grid size={20} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 ${
                viewMode === 'list'
                  ? 'bg-primary-50 text-primary-600'
                  : 'bg-white text-gray-600'
              } transition-colors border-r border-gray-300`}
              aria-label="תצוגת רשימה"
            >
              <List size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Active filters chips */}
      {hasActiveFilters() && (
        <div className="flex flex-wrap gap-2 mb-4">
          {filters.startDate && (
            <div className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center gap-2">
              מ-{formatDateIL(filters.startDate)}
              <button onClick={() => updateFilter('startDate', undefined)}>
                <X size={14} />
              </button>
            </div>
          )}
          {filters.endDate && (
            <div className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center gap-2">
              עד-{formatDateIL(filters.endDate)}
              <button onClick={() => updateFilter('endDate', undefined)}>
                <X size={14} />
              </button>
            </div>
          )}
          {filters.categoryIds && filters.categoryIds.length > 0 && (
            <div className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm flex items-center gap-2">
              {filters.categoryIds.length} קטגוריות
              <button onClick={() => updateFilter('categoryIds', undefined)}>
                <X size={14} />
              </button>
            </div>
          )}
          <button
            onClick={handleClearFilters}
            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 underline"
          >
            נקה הכל
          </button>
        </div>
      )}

      {/* Receipts grid/list */}
      {receipts.length === 0 && !isLoadingList ? (
        <>
          {/* No receipts at all */}
          {!searchQuery && !hasActiveFilters() && (
            <EmptyState
              icon={ReceiptIcon}
              title="הארכיון ריק"
              description="לאחר שתאשר קבלות, הן יופיעו כאן. התחל על ידי העלאת קבלה חדשה."
              actionLabel="העלה קבלה"
              onAction={() => navigate('/receipts/new')}
            />
          )}

          {/* No search results */}
          {searchQuery && !hasActiveFilters() && (
            <EmptyState
              icon={Search}
              title="לא נמצאו תוצאות"
              description={`לא מצאנו קבלות התואמות את החיפוש "${searchQuery}"`}
              actionLabel="נקה חיפוש"
              onAction={() => setSearchQuery('')}
            />
          )}

          {/* No results after filtering */}
          {hasActiveFilters() && (
            <EmptyState
              icon={Filter}
              title="אין קבלות בסינון זה"
              description="נסה להרחיב את הפילטרים או לבחור טווח תאריכים אחר"
              actionLabel="נקה פילטרים"
              onAction={handleClearFilters}
            />
          )}
        </>
      ) : (
        <>
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {receipts.map((receipt) => {
                const category = DEFAULT_CATEGORIES.find(
                  (c) => c.id === receipt.categoryId
                );
                return (
                  <Card
                    key={receipt.id}
                    shadow="sm"
                    padding="none"
                    hoverable
                    onClick={() => navigate(`/receipts/${receipt.id}`)}
                    className="cursor-pointer overflow-hidden"
                  >
                    {/* Image preview */}
                    <div className="aspect-[16/9] bg-gray-100 overflow-hidden">
                      <img
                        src={receipt.imageUrl}
                        alt={receipt.vendorName}
                        className="w-full h-full object-cover"
                      />
                    </div>

                    {/* Content */}
                    <div className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-600 text-gray-900 truncate flex-1">
                          {receipt.vendorName}
                        </h3>
                        {category && (
                          <div
                            className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-lg"
                            style={{
                              backgroundColor: `${category.color}20`
                            }}
                          >
                            {category.icon}
                          </div>
                        )}
                      </div>

                      <p className="text-2xl font-700 text-gray-900 mb-2">
                        {formatAmount(receipt.totalAmount)}
                      </p>

                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <span className="flex items-center gap-1">
                          <Calendar size={14} />
                          {formatDateIL(receipt.date)}
                        </span>
                        {category && (
                          <span
                            className="text-xs"
                            style={{ color: category.color }}
                          >
                            {category.nameHe}
                          </span>
                        )}
                      </div>
                    </div>
                  </Card>
                );
              })}
            </div>
          ) : (
            <div className="space-y-3">
              {receipts.map((receipt) => {
                const category = DEFAULT_CATEGORIES.find(
                  (c) => c.id === receipt.categoryId
                );
                return (
                  <Card
                    key={receipt.id}
                    shadow="sm"
                    padding="md"
                    hoverable
                    onClick={() => navigate(`/receipts/${receipt.id}`)}
                    className="cursor-pointer"
                  >
                    <div className="flex items-center gap-4">
                      {/* Thumbnail */}
                      <div className="w-20 h-20 rounded-lg bg-gray-100 overflow-hidden flex-shrink-0">
                        <img
                          src={receipt.imageUrl}
                          alt={receipt.vendorName}
                          className="w-full h-full object-cover"
                        />
                      </div>

                      {/* Info */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-1">
                          <h3 className="font-600 text-gray-900 truncate">
                            {receipt.vendorName}
                          </h3>
                          <p className="text-xl font-700 text-gray-900 flex-shrink-0 ml-4">
                            {formatAmount(receipt.totalAmount)}
                          </p>
                        </div>

                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <span className="flex items-center gap-1">
                            <Calendar size={14} />
                            {formatDateIL(receipt.date)}
                          </span>
                          {category && (
                            <span
                              className="flex items-center gap-1"
                              style={{ color: category.color }}
                            >
                              <Tag size={14} />
                              {category.nameHe}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}

          {/* Loading more indicator */}
          {loadingMore && (
            <div className="py-8">
              <LoadingSpinner text="טוען קבלות נוספות..." />
            </div>
          )}
        </>
      )}

      {/* Filter Modal */}
      <Modal
        isOpen={showFilterModal}
        onClose={() => setShowFilterModal(false)}
        title="סינון קבלות"
        size="md"
        footer={
          <div className="flex gap-3">
            <Button variant="secondary" fullWidth onClick={handleClearFilters}>
              נקה הכל
            </Button>
            <Button variant="primary" fullWidth onClick={applyFilters}>
              החל סינון
            </Button>
          </div>
        }
      >
        <div className="space-y-6">
          {/* Date range */}
          <div>
            <label className="block text-sm font-600 text-gray-700 mb-3">
              <Calendar size={18} className="inline ml-2" />
              טווח תאריכים
            </label>
            <div className="grid grid-cols-2 gap-3">
              <Input
                type="date"
                label="מתאריך"
                value={dateRange.start}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setDateRange((prev) => ({ ...prev, start: e.target.value }))
                }
              />
              <Input
                type="date"
                label="עד תאריך"
                value={dateRange.end}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setDateRange((prev) => ({ ...prev, end: e.target.value }))
                }
              />
            </div>
          </div>

          {/* Categories */}
          <div>
            <label className="block text-sm font-600 text-gray-700 mb-3">
              <Tag size={18} className="inline ml-2" />
              קטגוריות
            </label>
            <div className="grid grid-cols-2 gap-2">
              {DEFAULT_CATEGORIES.map((category) => {
                const isSelected = selectedCategories.includes(category.id);
                return (
                  <button
                    key={category.id}
                    onClick={() => {
                      setSelectedCategories((prev) =>
                        isSelected
                          ? prev.filter((id) => id !== category.id)
                          : [...prev, category.id]
                      );
                    }}
                    className={`
                      p-3 rounded-lg border-2 text-right transition-all
                      ${
                        isSelected
                          ? 'border-primary-600 bg-primary-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                  >
                    <div className="flex items-center gap-2">
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-lg"
                        style={{
                          backgroundColor: `${category.color}20`
                        }}
                      >
                        {category.icon}
                      </div>
                      <span className="text-sm font-500">
                        {category.nameHe}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Amount range */}
          <div>
            <label className="block text-sm font-600 text-gray-700 mb-3">
              <DollarSign size={18} className="inline ml-2" />
              טווח סכומים
            </label>
            <div className="grid grid-cols-2 gap-3">
              <Input
                type="number"
                label="סכום מינימלי"
                placeholder="0"
                value={amountRange.min}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setAmountRange((prev) => ({ ...prev, min: e.target.value }))
                }
                icon={<span className="text-gray-500">₪</span>}
              />
              <Input
                type="number"
                label="סכום מקסימלי"
                placeholder="1000"
                value={amountRange.max}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setAmountRange((prev) => ({ ...prev, max: e.target.value }))
                }
                icon={<span className="text-gray-500">₪</span>}
              />
            </div>
          </div>
        </div>
      </Modal>

      {/* Sort Modal */}
      <Modal
        isOpen={showSortModal}
        onClose={() => setShowSortModal(false)}
        title="מיון קבלות"
        size="sm"
      >
        <div className="space-y-2">
          {[
            { field: 'date' as ReceiptSortField, label: 'תאריך' },
            { field: 'amount' as ReceiptSortField, label: 'סכום' },
            { field: 'vendor' as ReceiptSortField, label: 'שם עסק' },
            { field: 'createdAt' as ReceiptSortField, label: 'תאריך העלאה' }
          ].map((option) => (
            <div key={option.field} className="space-y-1">
              <button
                onClick={() => handleSort(option.field, 'desc')}
                className={`
                  w-full p-3 rounded-lg border-2 text-right transition-all
                  ${
                    sortField === option.field && sortOrder === 'desc'
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                {option.label} (מהגבוה לנמוך)
              </button>
              <button
                onClick={() => handleSort(option.field, 'asc')}
                className={`
                  w-full p-3 rounded-lg border-2 text-right transition-all
                  ${
                    sortField === option.field && sortOrder === 'asc'
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                {option.label} (מהנמוך לגבוה)
              </button>
            </div>
          ))}
        </div>
      </Modal>
    </PageContainer>
  );
};

export default ArchivePage;
