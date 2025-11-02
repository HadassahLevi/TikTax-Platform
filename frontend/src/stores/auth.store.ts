/**
 * Authentication Store (Zustand)
 * CRITICAL: Tokens stored in MEMORY ONLY (never localStorage)
 * Security requirement for Tik-Tax
 */

import { create } from 'zustand';

interface AuthState {
  // State
  accessToken: string | null;
  refreshToken: string | null;
  user: any | null; // TODO: Replace with User type
  isAuthenticated: boolean;

  // Actions
  setTokens: (accessToken: string, refreshToken: string) => void;
  setUser: (user: any) => void;
  clearAuth: () => void;
  getAccessToken: () => string | null;
}

/**
 * Auth Store - Tokens in Memory Only
 * 🔒 NEVER use localStorage for sensitive data
 */
export const useAuthStore = create<AuthState>((set, get) => ({
  // Initial State
  accessToken: null,
  refreshToken: null,
  user: null,
  isAuthenticated: false,

  // Set authentication tokens
  setTokens: (accessToken: string, refreshToken: string) => {
    set({
      accessToken,
      refreshToken,
      isAuthenticated: true,
    });
  },

  // Set user data
  setUser: (user: any) => {
    set({ user });
  },

  // Clear authentication (logout)
  clearAuth: () => {
    set({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
    });
  },

  // Get current access token
  getAccessToken: () => {
    return get().accessToken;
  },
}));
