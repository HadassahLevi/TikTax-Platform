/**
 * Services Index
 * 
 * Central export point for all service modules.
 * Makes imports cleaner throughout the application.
 * 
 * @example
 * ```typescript
 * import { authService } from '@/services';
 * 
 * await authService.login({ email, password });
 * ```
 */

// Export all auth service functions
export * from './auth.service';

// Export auth service as default for convenience
export { default as authService } from './auth.service';

// Export all receipt service functions
export * from './receipt.service';

// Export all export service functions
export * from './export.service';

// Export all receipt service functions
export * from './receipt.service';

// Export receipt service as default for convenience
export { default as receiptService } from './receipt.service';
