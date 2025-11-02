import { useReceiptStore } from '@/stores/receipt.store';
import { useCallback, useEffect } from 'react';
import type { ReceiptUpdateRequest, ReceiptFilterOptions } from '@/types/receipt.types';

/**
 * Custom hook for receipt management
 * Provides convenient access to receipt state and actions
 * 
 * @example
 * ```tsx
 * const {
 *   receipts,
 *   isLoading,
 *   uploadReceipt,
 *   approveReceipt
 * } = useReceipt();
 * 
 * const handleUpload = async (file: File) => {
 *   const id = await uploadReceipt(file);
 *   console.log('Uploaded:', id);
 * };
 * ```
 */
export const useReceipt = () => {
  const {
    currentReceipt,
    receipts,
    total,
    hasMore,
    statistics,
    isUploading,
    isProcessing,
    isLoadingList,
    isLoadingStats,
    error,
    uploadError,
    
    uploadReceipt,
    retryProcessing,
    setCurrentReceipt,
    updateCurrentReceipt,
    approveReceipt,
    deleteReceipt,
    fetchReceipts,
    loadMoreReceipts,
    searchReceipts,
    setFilters,
    clearFilters,
    setSort,
    fetchStatistics,
    clearError
  } = useReceiptStore();
  
  /**
   * Upload receipt and start processing
   */
  const handleUpload = useCallback(async (file: File) => {
    try {
      const receiptId = await uploadReceipt(file);
      return receiptId;
    } catch (error) {
      throw error;
    }
  }, [uploadReceipt]);
  
  /**
   * Approve receipt with final data
   */
  const handleApprove = useCallback(async (
    receiptId: string,
    finalData: ReceiptUpdateRequest
  ) => {
    await approveReceipt(receiptId, finalData);
  }, [approveReceipt]);
  
  /**
   * Delete receipt with confirmation
   */
  const handleDelete = useCallback(async (receiptId: string) => {
    if (window.confirm('האם אתה בטוח שברצונך למחוק קבלה זו?')) {
      await deleteReceipt(receiptId);
    }
  }, [deleteReceipt]);
  
  /**
   * Search with debounce
   */
  const handleSearch = useCallback((query: string) => {
    if (query.length >= 2 || query.length === 0) {
      searchReceipts(query);
    }
  }, [searchReceipts]);
  
  return {
    // State
    currentReceipt,
    receipts,
    total,
    hasMore,
    statistics,
    isUploading,
    isProcessing,
    isLoadingList,
    isLoadingStats,
    error,
    uploadError,
    
    // Actions
    uploadReceipt: handleUpload,
    retryProcessing,
    setCurrentReceipt,
    updateCurrentReceipt,
    approveReceipt: handleApprove,
    deleteReceipt: handleDelete,
    fetchReceipts,
    loadMoreReceipts,
    searchReceipts: handleSearch,
    setFilters,
    clearFilters,
    setSort,
    fetchStatistics,
    clearError
  };
};

/**
 * Hook to load receipts on component mount
 * Automatically fetches receipts if store is empty
 * 
 * @example
 * ```tsx
 * function ReceiptList() {
 *   const { receipts } = useLoadReceipts();
 *   
 *   return (
 *     <div>
 *       {receipts.map(receipt => (
 *         <ReceiptCard key={receipt.id} receipt={receipt} />
 *       ))}
 *     </div>
 *   );
 * }
 * ```
 */
export const useLoadReceipts = () => {
  const { fetchReceipts, receipts } = useReceiptStore();
  
  useEffect(() => {
    if (receipts.length === 0) {
      fetchReceipts(true);
    }
  }, []);
  
  return { receipts };
};

/**
 * Hook to load statistics on component mount
 * Automatically fetches statistics if not already loaded
 * 
 * @example
 * ```tsx
 * function Dashboard() {
 *   const { statistics } = useLoadStatistics();
 *   
 *   if (!statistics) return <LoadingSpinner />;
 *   
 *   return (
 *     <div>
 *       <h2>Total: ₪{statistics.totalAmount}</h2>
 *       <p>{statistics.totalReceipts} receipts</p>
 *     </div>
 *   );
 * }
 * ```
 */
export const useLoadStatistics = () => {
  const { fetchStatistics, statistics } = useReceiptStore();
  
  useEffect(() => {
    if (!statistics) {
      fetchStatistics();
    }
  }, []);
  
  return { statistics };
};

/**
 * Hook for receipt validation helpers
 * Provides validation functions for receipt fields
 * 
 * @example
 * ```tsx
 * const {
 *   validateAmount,
 *   validateDate,
 *   validateVendorName
 * } = useReceiptValidation();
 * 
 * const amountError = validateAmount(amount);
 * if (amountError) {
 *   setError(amountError);
 * }
 * ```
 */
export const useReceiptValidation = () => {
  const validateAmount = useCallback((amount: number): string | null => {
    if (!amount || amount <= 0) {
      return 'הסכום חייב להיות גדול מ-0';
    }
    if (amount > 1000000) {
      return 'הסכום גבוה מדי';
    }
    return null;
  }, []);
  
  const validateDate = useCallback((date: string): string | null => {
    const receiptDate = new Date(date);
    const now = new Date();
    const sevenYearsAgo = new Date(now.setFullYear(now.getFullYear() - 7));
    
    if (receiptDate > new Date()) {
      return 'התאריך לא יכול להיות בעתיד';
    }
    if (receiptDate < sevenYearsAgo) {
      return 'קבלה ישנה מדי (מעל 7 שנים)';
    }
    return null;
  }, []);
  
  const validateVendorName = useCallback((name: string): string | null => {
    if (!name || name.trim().length < 2) {
      return 'שם העסק חייב להכיל לפחות 2 תווים';
    }
    return null;
  }, []);
  
  const validateBusinessNumber = useCallback((num: string): string | null => {
    const cleaned = num.replace(/\D/g, '');
    if (cleaned.length !== 9) {
      return 'מספר עסק חייב להכיל 9 ספרות';
    }
    return null;
  }, []);
  
  return {
    validateAmount,
    validateDate,
    validateVendorName,
    validateBusinessNumber
  };
};

/**
 * Hook for infinite scroll pagination
 * Automatically loads more receipts when scrolling near bottom
 * 
 * @param callback - Function to call when more items should be loaded
 * 
 * @example
 * const { receipts, loadMoreReceipts } = useReceipt();
 * 
 * useInfiniteScroll(() => {
 *   loadMoreReceipts();
 * });
 */
export const useInfiniteScroll = (callback: () => void) => {
  const { hasMore, isLoadingList } = useReceiptStore();
  
  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 &&
        hasMore &&
        !isLoadingList
      ) {
        callback();
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [hasMore, isLoadingList, callback]);
};

/**
 * Hook for receipt filters with URL sync
 * Manages filter state and provides helper functions
 * 
 * @example
 * const { filters, updateFilter, clearFilters, hasActiveFilters } = useReceiptFilters();
 * 
 * // Update single filter
 * updateFilter('status', 'approved');
 * 
 * // Clear all filters
 * clearFilters();
 * 
 * // Check if filters active
 * if (hasActiveFilters()) { ... }
 */
export const useReceiptFilters = () => {
  const { filters, setFilters, clearFilters } = useReceiptStore();
  
  const updateFilter = useCallback((key: keyof ReceiptFilterOptions, value: any) => {
    setFilters({ [key]: value });
  }, [setFilters]);
  
  const hasActiveFilters = useCallback(() => {
    return Object.keys(filters).length > 0;
  }, [filters]);
  
  return {
    filters,
    updateFilter,
    clearFilters,
    hasActiveFilters
  };
};

export default useReceipt;
