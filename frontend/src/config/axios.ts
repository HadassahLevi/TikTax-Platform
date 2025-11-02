/**
 * Axios HTTP Client Configuration
 * Configured instance with interceptors for authentication and error handling
 */

import axios, { AxiosError } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';
import config from './index';
import { useAuthStore } from '../stores/auth.store';

// Extend AxiosRequestConfig to include custom properties
interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
  _requestStartTime?: number;
}

/**
 * Create Axios instance with base configuration
 */
const axiosInstance = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * REQUEST INTERCEPTOR
 * - Attach authentication token from Zustand store (NOT localStorage!)
 * - Add request timestamp for performance tracking
 */
axiosInstance.interceptors.request.use(
  (config: CustomAxiosRequestConfig) => {
    // Get access token from auth store (memory only - never localStorage!)
    const accessToken = useAuthStore.getState().getAccessToken();
    
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    // Add request timestamp for performance tracking
    config._requestStartTime = Date.now();

    return config;
  },
  (error: AxiosError) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

/**
 * RESPONSE INTERCEPTOR
 * - Log slow responses (>3 seconds)
 * - Handle 401: Auto token refresh and retry
 * - Handle 403: Access denied logging
 * - Handle network errors
 */
axiosInstance.interceptors.response.use(
  (response) => {
    // Performance tracking - log slow responses
    const requestStartTime = (response.config as CustomAxiosRequestConfig)._requestStartTime;
    if (requestStartTime) {
      const duration = Date.now() - requestStartTime;
      if (duration > 3000) {
        console.warn(
          `⚠️ Slow Response: ${response.config.url} took ${duration}ms`
        );
      }
    }

    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as CustomAxiosRequestConfig;

    // Network error (no response from server)
    if (!error.response) {
      console.error('❌ Network Error: Unable to connect to server', {
        url: originalRequest?.url,
        message: error.message,
      });
      return Promise.reject(error);
    }

    const { status } = error.response;

    // Handle 401 Unauthorized - Token expired/invalid
    if (status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Attempt to refresh token
        const refreshToken = useAuthStore.getState().refreshToken;
        
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        // Call refresh token endpoint
        const response = await axios.post(
          `${config.apiBaseUrl}/auth/refresh`,
          { refreshToken }
        );

        const { accessToken, refreshToken: newRefreshToken } = response.data;

        // Update tokens in store (memory only!)
        useAuthStore.getState().setTokens(accessToken, newRefreshToken);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Refresh failed - clear auth and redirect to login
        console.error('❌ Token Refresh Failed:', refreshError);
        
        // Clear authentication state
        useAuthStore.getState().clearAuth();
        
        // Redirect to login page
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        
        return Promise.reject(refreshError);
      }
    }

    // Handle 403 Forbidden - Access denied
    if (status === 403) {
      console.error('❌ Access Denied (403):', {
        url: originalRequest?.url,
        message: error.response.data,
      });
    }

    // Handle 404 Not Found
    if (status === 404) {
      console.error('❌ Resource Not Found (404):', originalRequest?.url);
    }

    // Handle 500 Server Error
    if (status >= 500) {
      console.error('❌ Server Error:', {
        status,
        url: originalRequest?.url,
        message: error.response.data,
      });
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
