import api from '@/config/axios';

export interface Notification {
  id: number;
  user_id: number;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  action_url?: string;
  action_label?: string;
  is_read: boolean;
  read_at?: string;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: Notification[];
  total: number;
  unread_count: number;
}

const notificationService = {
  /**
   * Get user notifications with pagination
   */
  getNotifications: async (
    skip = 0,
    limit = 20,
    unreadOnly = false
  ): Promise<NotificationListResponse> => {
    const response = await api.get('/notifications', {
      params: { skip, limit, unread_only: unreadOnly }
    });
    return response.data;
  },

  /**
   * Get unread notification count (for badge)
   */
  getUnreadCount: async (): Promise<number> => {
    const response = await api.get('/notifications/unread-count');
    return response.data.unread_count;
  },

  /**
   * Mark a notification as read
   */
  markAsRead: async (notificationId: number): Promise<Notification> => {
    const response = await api.put(`/notifications/${notificationId}/read`);
    return response.data;
  },

  /**
   * Mark all notifications as read
   */
  markAllAsRead: async (): Promise<{ message: string; updated_count: number }> => {
    const response = await api.post('/notifications/mark-all-read');
    return response.data;
  },

  /**
   * Delete a notification
   */
  deleteNotification: async (notificationId: number): Promise<void> => {
    await api.delete(`/notifications/${notificationId}`);
  },

  /**
   * Delete all notifications
   */
  deleteAllNotifications: async (): Promise<{ message: string; deleted_count: number }> => {
    const response = await api.delete('/notifications/delete-all');
    return response.data;
  }
};

export default notificationService;
