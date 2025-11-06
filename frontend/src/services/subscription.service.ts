/**
 * Subscription Service
 * 
 * Handles all subscription and billing operations:
 * - Checkout session creation
 * - Billing history retrieval
 * - Subscription cancellation
 * - Billing portal access
 * 
 * @module services/subscriptionService
 */

import api from '@/config/axios';

/**
 * Invoice interface for billing history
 */
export interface Invoice {
  id: string;
  date: string;
  amount: number;
  currency: string;
  status: string;
  invoice_pdf?: string;
  hosted_invoice_url?: string;
}

/**
 * Checkout session response
 */
export interface CheckoutSessionResponse {
  session_id: string;
  checkout_url: string;
}

/**
 * Subscription status response
 */
export interface SubscriptionStatus {
  user_id: number;
  subscription_plan: string;
  subscription_status: string;
  subscription_start_date?: string;
  subscription_end_date?: string;
  receipt_limit: number;
  receipts_used_this_month: number;
}

/**
 * Cancellation response
 */
export interface CancellationResponse {
  status: string;
  ends_at?: string;
  message: string;
}

/**
 * Billing portal response
 */
export interface BillingPortalResponse {
  portal_url: string;
}

/**
 * Create Stripe checkout session for subscription upgrade
 * 
 * @param data - Checkout data with price_id and billing_cycle
 * @returns Checkout session with redirect URL
 * 
 * @example
 * ```typescript
 * const { checkout_url } = await createCheckout({
 *   price_id: 'price_123',
 *   billing_cycle: 'monthly'
 * });
 * window.location.href = checkout_url;
 * ```
 */
export const createCheckout = async (data: {
  price_id: string;
  billing_cycle: 'monthly' | 'yearly';
}): Promise<CheckoutSessionResponse> => {
  const response = await api.post('/subscriptions/upgrade', data);
  return response.data;
};

/**
 * Get current subscription status
 * 
 * @returns Current subscription details
 * 
 * @example
 * ```typescript
 * const status = await getSubscriptionStatus();
 * console.log(`Plan: ${status.subscription_plan}`);
 * ```
 */
export const getSubscriptionStatus = async (): Promise<SubscriptionStatus> => {
  const response = await api.get('/subscriptions/status');
  return response.data;
};

/**
 * Get billing history (past invoices)
 * 
 * @param limit - Number of invoices to fetch (default: 10)
 * @returns Array of invoice details
 * 
 * @example
 * ```typescript
 * const invoices = await getBillingHistory(10);
 * invoices.forEach(inv => {
 *   console.log(`${inv.date}: ₪${inv.amount}`);
 * });
 * ```
 */
export const getBillingHistory = async (limit: number = 10): Promise<Invoice[]> => {
  const response = await api.get(`/subscriptions/billing-history?limit=${limit}`);
  return response.data;
};

/**
 * Cancel active subscription
 * 
 * Subscription will remain active until the end of the current billing period.
 * 
 * @returns Cancellation details with effective date
 * 
 * @example
 * ```typescript
 * const result = await cancelSubscription();
 * console.log(result.message);
 * console.log(`Ends at: ${result.ends_at}`);
 * ```
 */
export const cancelSubscription = async (): Promise<CancellationResponse> => {
  const response = await api.post('/subscriptions/cancel');
  return response.data;
};

/**
 * Get Stripe billing portal URL
 * 
 * Redirects user to Stripe-hosted portal where they can:
 * - Update payment methods
 * - View billing history
 * - Download invoices
 * - Update billing information
 * 
 * @returns Portal URL for redirect
 * 
 * @example
 * ```typescript
 * const { portal_url } = await getBillingPortal();
 * window.location.href = portal_url;
 * ```
 */
export const getBillingPortal = async (): Promise<BillingPortalResponse> => {
  const response = await api.get('/subscriptions/billing-portal');
  return response.data;
};

/**
 * Default export with all methods
 */
const subscriptionService = {
  createCheckout,
  getSubscriptionStatus,
  getBillingHistory,
  cancelSubscription,
  getBillingPortal,
};

export default subscriptionService;
