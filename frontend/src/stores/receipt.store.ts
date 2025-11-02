/**
 * Receipt Management Store (Zustand)
 * 
 * Central state management for receipt upload, processing, archiving, and filtering.
 * 
 * Features:
 * - Upload with progress tracking
 * - Automatic polling for OCR processing status
 * - Pagination support (infinite scroll)
 * - Search functionality with debounce
 * - Advanced filters and sorting
 * - Statistics caching
 * - Error handling with Hebrew messages
 * - Optimistic updates for delete
 * - DevTools integration for debugging
 * 
 * @module stores/receipt.store
 * 
 * Usage Examples:
 * ```typescript
 * // In component
 * import { useReceiptStore } from '@/stores/receipt.store';
 * 
 * const MyComponent = () => {
 *   const { uploadReceipt, receipts, isUploading } = useReceiptStore();
 *   
 *   const handleFileUpload = async (file: File) => {
 *     const receiptId = await uploadReceipt(file);
 *     // Polling starts automatically
 *   };
 *   
 *   return (
 *     <div>
 *       {isUploading && <Spinner />}
 *       {receipts.map(receipt => <ReceiptCard key={receipt.id} {...receipt} />)}
 *     </div>
 *   );
 * };
 * 
 * // With selectors
 * const receipts = useReceiptStore(selectReceipts);
 * const isLoading = useReceiptStore(selectIsLoading);
 * ```
 */

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import type {
  Receipt,
  ReceiptFilterOptions,
  ReceiptSortOptions,
  ReceiptStatistics,
  ReceiptUpdateRequest
} from '@/types/receipt.types';
import * as receiptService from '@/services/receipt.service';

// ============================================================================
// STATE INTERFACE
// ============================================================================

interface ReceiptState {
  // Current receipt being processed/edited
  currentReceipt: Receipt | null;
  
  // Receipt list (archive)
  receipts: Receipt[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
  
  // Filters and sorting
  filters: ReceiptFilterOptions;
  sort: ReceiptSortOptions;
  searchQuery: string;
  
  // Statistics
  statistics: ReceiptStatistics | null;
  
  // Loading states
  isUploading: boolean;
  isProcessing: boolean;
  isLoadingList: boolean;
  isLoadingStats: boolean;
  
  // Errors
  error: string | null;
  uploadError: string | null;
  
  // Polling control
  pollingIntervalId: number | null;
}

// ============================================================================
// ACTIONS INTERFACE
// ============================================================================

interface ReceiptActions {
  // Upload & Processing
  uploadReceipt: (file: File) => Promise<string>; // Returns receiptId
  pollProcessingStatus: (receiptId: string) => Promise<void>;
  stopPolling: () => void;
  retryProcessing: (receiptId: string) => Promise<void>;
  
  // Current receipt management
  setCurrentReceipt: (receipt: Receipt | null) => void;
  updateCurrentReceipt: (data: ReceiptUpdateRequest) => Promise<void>;
  approveReceipt: (receiptId: string, finalData: ReceiptUpdateRequest) => Promise<void>;
  deleteReceipt: (receiptId: string) => Promise<void>;
  
  // Receipt list (archive)
  fetchReceipts: (reset?: boolean) => Promise<void>;
  loadMoreReceipts: () => Promise<void>;
  searchReceipts: (query: string) => Promise<void>;
  
  // Filters & Sort
  setFilters: (filters: Partial<ReceiptFilterOptions>) => void;
  clearFilters: () => void;
  setSort: (sort: ReceiptSortOptions) => void;
  
  // Statistics
  fetchStatistics: () => Promise<void>;
  
  // Helpers
  setError: (error: string | null) => void;
  clearError: () => void;
  reset: () => void;
}

type ReceiptStore = ReceiptState & ReceiptActions;

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: ReceiptState = {
  currentReceipt: null,
  receipts: [],
  total: 0,
  page: 1,
  pageSize: 20,
  hasMore: false,
  filters: {},
  sort: { field: 'date', order: 'desc' },
  searchQuery: '',
  statistics: null,
  isUploading: false,
  isProcessing: false,
  isLoadingList: false,
  isLoadingStats: false,
  error: null,
  uploadError: null,
  pollingIntervalId: null
};

// ============================================================================
// STORE IMPLEMENTATION
// ============================================================================

export const useReceiptStore = create<ReceiptStore>()(
  devtools(
    (set, get) => ({
      ...initialState,
      
      // ======================================================================
      // UPLOAD RECEIPT
      // ======================================================================
      uploadReceipt: async (file: File) => {
        set({ isUploading: true, uploadError: null, error: null });
        try {
          const response = await receiptService.uploadReceipt(file);
          set({ isUploading: false });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Upload successful:', response.receiptId);
          }
          
          // Start polling for processing status
          get().pollProcessingStatus(response.receiptId);
          
          return response.receiptId;
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בהעלאת הקבלה';
          set({ isUploading: false, uploadError: errorMessage });
          throw error;
        }
      },
      
      // ======================================================================
      // POLL PROCESSING STATUS
      // ======================================================================
      pollProcessingStatus: async (receiptId: string) => {
        // Stop any existing polling
        get().stopPolling();
        
        set({ isProcessing: true, error: null });
        
        let attempts = 0;
        const maxAttempts = 30; // 30 attempts * 2 seconds = 60 seconds max
        
        const poll = async () => {
          attempts++;
          
          if (attempts > maxAttempts) {
            get().stopPolling();
            set({ 
              isProcessing: false, 
              error: 'העיבוד לוקח זמן רב מהרגיל. נסה שוב מאוחר יותר.' 
            });
            return;
          }
          
          try {
            const response = await receiptService.checkProcessingStatus(receiptId);
            
            if (import.meta.env.DEV) {
              console.log(`[Receipt Store] Polling attempt ${attempts}:`, response.status);
            }
            
            if (response.status === 'review' || response.status === 'approved') {
              // Processing complete - fetch full receipt data
              get().stopPolling();
              const receipt = await receiptService.getReceipt(receiptId);
              set({ 
                currentReceipt: receipt, 
                isProcessing: false 
              });
              
              if (import.meta.env.DEV) {
                console.log('[Receipt Store] Processing complete:', receipt);
              }
            } else if (response.status === 'failed') {
              // Processing failed
              get().stopPolling();
              set({ 
                isProcessing: false, 
                error: 'עיבוד הקבלה נכשל. נסה שוב.' 
              });
            } else if (response.status === 'duplicate') {
              // Duplicate detected
              get().stopPolling();
              const receipt = await receiptService.getReceipt(receiptId);
              set({ 
                currentReceipt: receipt,
                isProcessing: false,
                error: 'קבלה זו כבר קיימת במערכת'
              });
            }
            // Otherwise, keep polling (status === 'processing')
          } catch (error) {
            get().stopPolling();
            const errorMessage = error instanceof Error ? error.message : 'שגיאה בעיבוד';
            set({ isProcessing: false, error: errorMessage });
          }
        };
        
        // Start polling every 2 seconds
        const intervalId = window.setInterval(poll, 2000);
        set({ pollingIntervalId: intervalId });
        
        // Poll immediately for first check
        poll();
      },
      
      // ======================================================================
      // STOP POLLING
      // ======================================================================
      stopPolling: () => {
        const { pollingIntervalId } = get();
        if (pollingIntervalId) {
          window.clearInterval(pollingIntervalId);
          set({ pollingIntervalId: null });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Polling stopped');
          }
        }
      },
      
      // ======================================================================
      // RETRY PROCESSING
      // ======================================================================
      retryProcessing: async (receiptId: string) => {
        set({ isProcessing: true, error: null });
        try {
          await receiptService.retryProcessing(receiptId);
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Retry processing initiated:', receiptId);
          }
          
          // Start polling again
          get().pollProcessingStatus(receiptId);
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בניסיון חוזר';
          set({ isProcessing: false, error: errorMessage });
          throw error;
        }
      },
      
      // ======================================================================
      // SET CURRENT RECEIPT
      // ======================================================================
      setCurrentReceipt: (receipt) => {
        set({ currentReceipt: receipt });
        
        if (import.meta.env.DEV) {
          console.log('[Receipt Store] Current receipt set:', receipt?.id);
        }
      },
      
      // ======================================================================
      // UPDATE CURRENT RECEIPT
      // ======================================================================
      updateCurrentReceipt: async (data: ReceiptUpdateRequest) => {
        const { currentReceipt } = get();
        if (!currentReceipt) {
          throw new Error('אין קבלה נבחרת');
        }
        
        set({ error: null });
        try {
          const updated = await receiptService.updateReceipt(currentReceipt.id, data);
          set({ currentReceipt: updated });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Receipt updated:', updated.id);
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בעדכון';
          set({ error: errorMessage });
          throw error;
        }
      },
      
      // ======================================================================
      // APPROVE RECEIPT
      // ======================================================================
      approveReceipt: async (receiptId: string, finalData: ReceiptUpdateRequest) => {
        set({ isProcessing: true, error: null });
        try {
          const approved = await receiptService.approveReceipt(receiptId, finalData);
          
          // Update state
          set({ 
            currentReceipt: approved, 
            isProcessing: false,
            // Add to receipts list (at the beginning)
            receipts: [approved, ...get().receipts],
            total: get().total + 1
          });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Receipt approved:', approved.id);
          }
          
          // Refresh statistics
          get().fetchStatistics();
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה באישור';
          set({ isProcessing: false, error: errorMessage });
          throw error;
        }
      },
      
      // ======================================================================
      // DELETE RECEIPT
      // ======================================================================
      deleteReceipt: async (receiptId: string) => {
        set({ error: null });
        
        // Optimistic update - store current state for rollback
        const previousReceipts = get().receipts;
        const previousTotal = get().total;
        const previousCurrent = get().currentReceipt;
        
        // Update UI immediately
        set({
          receipts: get().receipts.filter(r => r.id !== receiptId),
          total: get().total - 1,
          currentReceipt: get().currentReceipt?.id === receiptId ? null : get().currentReceipt
        });
        
        try {
          await receiptService.deleteReceipt(receiptId);
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Receipt deleted:', receiptId);
          }
          
          // Refresh statistics
          get().fetchStatistics();
        } catch (error) {
          // Rollback on error
          set({
            receipts: previousReceipts,
            total: previousTotal,
            currentReceipt: previousCurrent
          });
          
          const errorMessage = error instanceof Error ? error.message : 'שגיאה במחיקה';
          set({ error: errorMessage });
          throw error;
        }
      },
      
      // ======================================================================
      // FETCH RECEIPTS
      // ======================================================================
      fetchReceipts: async (reset = false) => {
        set({ isLoadingList: true, error: null });
        try {
          const { filters, sort, pageSize } = get();
          const page = reset ? 1 : get().page;
          
          const response = await receiptService.getReceipts(filters, sort, page, pageSize);
          
          set({
            receipts: reset ? response.receipts : [...get().receipts, ...response.receipts],
            total: response.total,
            page: response.page,
            hasMore: response.hasMore,
            isLoadingList: false
          });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Receipts fetched:', {
              page: response.page,
              count: response.receipts.length,
              total: response.total,
              hasMore: response.hasMore
            });
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בטעינת קבלות';
          set({ isLoadingList: false, error: errorMessage });
        }
      },
      
      // ======================================================================
      // LOAD MORE RECEIPTS (PAGINATION)
      // ======================================================================
      loadMoreReceipts: async () => {
        const { hasMore, isLoadingList } = get();
        
        if (!hasMore || isLoadingList) {
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Skip load more:', { hasMore, isLoadingList });
          }
          return;
        }
        
        set({ page: get().page + 1 });
        await get().fetchReceipts(false);
      },
      
      // ======================================================================
      // SEARCH RECEIPTS
      // ======================================================================
      searchReceipts: async (query: string) => {
        set({ searchQuery: query, isLoadingList: true, error: null });
        try {
          const response = await receiptService.searchReceipts(query, 1, get().pageSize);
          set({
            receipts: response.receipts,
            total: response.total,
            page: 1,
            hasMore: response.hasMore,
            isLoadingList: false
          });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Search complete:', {
              query,
              results: response.receipts.length
            });
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בחיפוש';
          set({ isLoadingList: false, error: errorMessage });
        }
      },
      
      // ======================================================================
      // SET FILTERS
      // ======================================================================
      setFilters: (filters: Partial<ReceiptFilterOptions>) => {
        const newFilters = { ...get().filters, ...filters };
        set({ 
          filters: newFilters,
          page: 1 
        });
        
        if (import.meta.env.DEV) {
          console.log('[Receipt Store] Filters updated:', newFilters);
        }
        
        get().fetchReceipts(true);
      },
      
      // ======================================================================
      // CLEAR FILTERS
      // ======================================================================
      clearFilters: () => {
        set({ filters: {}, searchQuery: '', page: 1 });
        
        if (import.meta.env.DEV) {
          console.log('[Receipt Store] Filters cleared');
        }
        
        get().fetchReceipts(true);
      },
      
      // ======================================================================
      // SET SORT
      // ======================================================================
      setSort: (sort: ReceiptSortOptions) => {
        set({ sort, page: 1 });
        
        if (import.meta.env.DEV) {
          console.log('[Receipt Store] Sort updated:', sort);
        }
        
        get().fetchReceipts(true);
      },
      
      // ======================================================================
      // FETCH STATISTICS
      // ======================================================================
      fetchStatistics: async () => {
        set({ isLoadingStats: true });
        try {
          const stats = await receiptService.getReceiptStatistics();
          set({ statistics: stats, isLoadingStats: false });
          
          if (import.meta.env.DEV) {
            console.log('[Receipt Store] Statistics fetched:', stats);
          }
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'שגיאה בטעינת סטטיסטיקות';
          set({ isLoadingStats: false, error: errorMessage });
        }
      },
      
      // ======================================================================
      // SET ERROR
      // ======================================================================
      setError: (error) => {
        set({ error });
        
        if (import.meta.env.DEV && error) {
          console.error('[Receipt Store] Error set:', error);
        }
      },
      
      // ======================================================================
      // CLEAR ERROR
      // ======================================================================
      clearError: () => {
        set({ error: null, uploadError: null });
      },
      
      // ======================================================================
      // RESET STORE
      // ======================================================================
      reset: () => {
        // Stop polling before reset
        get().stopPolling();
        
        set(initialState);
        
        if (import.meta.env.DEV) {
          console.log('[Receipt Store] Store reset');
        }
      }
    }),
    { name: 'receipt-store' }
  )
);

// ============================================================================
// SELECTORS
// ============================================================================

/**
 * Select current receipt being processed/edited
 */
export const selectCurrentReceipt = (state: ReceiptStore) => state.currentReceipt;

/**
 * Select receipts list
 */
export const selectReceipts = (state: ReceiptStore) => state.receipts;

/**
 * Select statistics
 */
export const selectStatistics = (state: ReceiptStore) => state.statistics;

/**
 * Select any loading state (for global loading indicator)
 */
export const selectIsLoading = (state: ReceiptStore) => 
  state.isUploading || state.isProcessing || state.isLoadingList || state.isLoadingStats;

/**
 * Select upload loading state
 */
export const selectIsUploading = (state: ReceiptStore) => state.isUploading;

/**
 * Select processing loading state
 */
export const selectIsProcessing = (state: ReceiptStore) => state.isProcessing;

/**
 * Select list loading state
 */
export const selectIsLoadingList = (state: ReceiptStore) => state.isLoadingList;

/**
 * Select pagination info
 */
export const selectPaginationInfo = (state: ReceiptStore) => ({
  page: state.page,
  pageSize: state.pageSize,
  total: state.total,
  hasMore: state.hasMore
});

/**
 * Select filters
 */
export const selectFilters = (state: ReceiptStore) => state.filters;

/**
 * Select sort options
 */
export const selectSort = (state: ReceiptStore) => state.sort;

/**
 * Select search query
 */
export const selectSearchQuery = (state: ReceiptStore) => state.searchQuery;

/**
 * Select error state
 */
export const selectError = (state: ReceiptStore) => state.error || state.uploadError;

/**
 * Select upload error specifically
 */
export const selectUploadError = (state: ReceiptStore) => state.uploadError;

/**
 * Select if filters are active
 */
export const selectHasActiveFilters = (state: ReceiptStore) => 
  Object.keys(state.filters).length > 0 || state.searchQuery.length > 0;

// ============================================================================
// HOOKS (CONVENIENCE)
// ============================================================================

/**
 * Hook to access receipt actions only (no re-renders on state changes)
 * 
 * Usage:
 * ```typescript
 * const actions = useReceiptActions();
 * actions.uploadReceipt(file);
 * ```
 */
export const useReceiptActions = () => {
  return useReceiptStore((state) => ({
    uploadReceipt: state.uploadReceipt,
    pollProcessingStatus: state.pollProcessingStatus,
    stopPolling: state.stopPolling,
    retryProcessing: state.retryProcessing,
    setCurrentReceipt: state.setCurrentReceipt,
    updateCurrentReceipt: state.updateCurrentReceipt,
    approveReceipt: state.approveReceipt,
    deleteReceipt: state.deleteReceipt,
    fetchReceipts: state.fetchReceipts,
    loadMoreReceipts: state.loadMoreReceipts,
    searchReceipts: state.searchReceipts,
    setFilters: state.setFilters,
    clearFilters: state.clearFilters,
    setSort: state.setSort,
    fetchStatistics: state.fetchStatistics,
    setError: state.setError,
    clearError: state.clearError,
    reset: state.reset
  }));
};

// ============================================================================
// CLEANUP UTILITY
// ============================================================================

/**
 * Clean up store on unmount (stop polling)
 * Call this in useEffect cleanup or when navigating away
 * 
 * Usage:
 * ```typescript
 * useEffect(() => {
 *   return () => cleanupReceiptStore();
 * }, []);
 * ```
 */
export const cleanupReceiptStore = () => {
  useReceiptStore.getState().stopPolling();
  
  if (import.meta.env.DEV) {
    console.log('[Receipt Store] Cleanup executed');
  }
};
