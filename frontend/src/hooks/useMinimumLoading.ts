import { useState, useEffect } from 'react';

/**
 * Hook to ensure loading states are displayed for a minimum duration
 * This prevents jarring flash effects when data loads too quickly
 * 
 * @param loading - The actual loading state from data fetching
 * @param minimumMs - Minimum time in milliseconds to show loading state (default: 300ms)
 * @returns boolean - Whether to show the loading state
 * 
 * @example
 * const { data, loading } = useFetchData();
 * const showLoading = useMinimumLoading(loading, 300);
 * 
 * if (showLoading) return <LoadingSpinner />;
 */
export const useMinimumLoading = (loading: boolean, minimumMs: number = 300): boolean => {
  const [showLoading, setShowLoading] = useState(loading);
  const [startTime, setStartTime] = useState<number | null>(null);

  useEffect(() => {
    if (loading) {
      // Start loading
      setShowLoading(true);
      setStartTime(Date.now());
    } else if (startTime !== null) {
      // Calculate elapsed time
      const elapsed = Date.now() - startTime;
      const remaining = minimumMs - elapsed;

      if (remaining > 0) {
        // Wait for remaining time
        const timeout = setTimeout(() => {
          setShowLoading(false);
          setStartTime(null);
        }, remaining);
        return () => clearTimeout(timeout);
      } else {
        // Minimum time already passed
        setShowLoading(false);
        setStartTime(null);
      }
    }
  }, [loading, minimumMs, startTime]);

  return showLoading;
};
