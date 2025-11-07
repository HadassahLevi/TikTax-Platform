/**
 * Profile & Settings Page
 * 
 * Comprehensive user profile management with three tabs:
 * - Profile: Personal and business information
 * - Security: Password, phone verification, sessions
 * - Subscription: Plan details, usage, billing history
 * 
 * Route: /profile
 * 
 * @page
 */

import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Modal from '@/components/ui/Modal';
import PageContainer from '@/components/layout/PageContainer';
import { useToast } from '@/hooks/useToast';
import { LoadingSpinner } from '@/components/loading/LoadingSpinner';
import { 
  User, 
  Lock, 
  CreditCard, 
  AlertTriangle, 
  CheckCircle, 
  Phone,
  Mail,
  Building,
  LogOut,
  Shield
} from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '@/utils/formatters';

// ============================================================================
// TYPES
// ============================================================================

interface ProfileFormData {
  fullName: string;
  businessName: string;
  businessNumber: string;
  phone: string;
}

interface PasswordFormData {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const ProfilePage: React.FC = () => {
  const { user, updateProfile, changePassword, deleteAccount, logout, usagePercentage, remainingReceipts } = useAuth();
  const navigate = useNavigate();
  const { showSuccess, showError } = useToast();
  
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'subscription'>('profile');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [loading, setLoading] = useState(false);
  
  // Profile form
  const profileForm = useForm<ProfileFormData>({
    defaultValues: {
      fullName: user?.fullName || '',
      businessName: user?.businessName || '',
      businessNumber: user?.businessNumber || '',
      phone: user?.phone || ''
    }
  });
  
  // Password form
  const passwordForm = useForm<PasswordFormData>({
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  });
  
  /**
   * Handle profile update submission
   */
  const handleProfileUpdate = async (data: ProfileFormData) => {
    setLoading(true);
    try {
      await updateProfile(data);
      showSuccess('הפרטים עודכנו בהצלחה');
    } catch (error) {
      showError(error instanceof Error ? error.message : 'שגיאה בעדכון הפרטים');
    } finally {
      setLoading(false);
    }
  };
  
  /**
   * Handle password change submission
   */
  const handlePasswordChange = async (data: PasswordFormData) => {
    // Validate password confirmation
    if (data.newPassword !== data.confirmPassword) {
      showError('הסיסמאות אינן תואמות');
      return;
    }
    
    // Validate password strength
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordRegex.test(data.newPassword)) {
      showError('הסיסמה חייבת להכיל לפחות 8 תווים, אות גדולה, אות קטנה, מספר ותו מיוחד');
      return;
    }
    
    setLoading(true);
    try {
      await changePassword(data.currentPassword, data.newPassword);
      setShowPasswordModal(false);
      passwordForm.reset();
      showSuccess('הסיסמה שונתה בהצלחה');
    } catch (error) {
      showError(error instanceof Error ? error.message : 'שגיאה בשינוי הסיסמה');
    } finally {
      setLoading(false);
    }
  };
  
  /**
   * Handle account deletion
   */
  const handleAccountDelete = async () => {
    setLoading(true);
    try {
      await deleteAccount();
      showSuccess('החשבון נמחק בהצלחה');
      navigate('/goodbye');
    } catch (error) {
      showError(error instanceof Error ? error.message : 'שגיאה במחיקת החשבון');
    } finally {
      setLoading(false);
    }
  };
  
  /**
   * Handle logout
   */
  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      // Silent fail, navigate anyway
      navigate('/login');
    }
  };
  
  // Loading state for initial data
  if (!user) {
    return (
      <PageContainer title="הגדרות">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg border border-gray-200 p-8">
            <LoadingSpinner size="lg" text="טוען נתונים..." />
          </div>
        </div>
      </PageContainer>
    );
  }
  
  return (
    <PageContainer
      title="הגדרות חשבון"
      subtitle="נהל את פרטי החשבון והגדרות האבטחה שלך"
      maxWidth="lg"
    >
      <div className="space-y-6">
        
        {/* Tab Navigation */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {/* Tab Buttons */}
          <div className="flex border-b border-gray-200 bg-gray-50">
            <TabButton
              active={activeTab === 'profile'}
              onClick={() => setActiveTab('profile')}
              icon={<User size={20} />}
              label="פרטים אישיים"
            />
            <TabButton
              active={activeTab === 'security'}
              onClick={() => setActiveTab('security')}
              icon={<Lock size={20} />}
              label="אבטחה"
            />
            <TabButton
              active={activeTab === 'subscription'}
              onClick={() => setActiveTab('subscription')}
              icon={<CreditCard size={20} />}
              label="מנוי"
            />
          </div>
          
          {/* Tab Content */}
          <div className="p-6">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === 'profile' && (
                <ProfileTab
                  form={profileForm}
                  onSubmit={handleProfileUpdate}
                  loading={loading}
                  user={user}
                />
              )}
              
              {activeTab === 'security' && (
                <SecurityTab
                  onPasswordChange={() => setShowPasswordModal(true)}
                  onLogout={handleLogout}
                  user={user}
                />
              )}
              
              {activeTab === 'subscription' && (
                <SubscriptionTab 
                  user={user}
                  usagePercentage={usagePercentage()}
                  remainingReceipts={remainingReceipts()}
                />
              )}
            </motion.div>
          </div>
        </div>
        
        {/* Danger Zone */}
        <div className="bg-red-50 border border-red-200 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-3">
            <AlertTriangle className="text-red-600" size={24} />
            <h3 className="text-lg font-semibold text-red-900">אזור מסוכן</h3>
          </div>
          <p className="text-red-700 text-sm mb-4">
            מחיקת החשבון תמחק לצמיתות את כל הנתונים שלך, כולל כל הקבלות והקבצים המאוחסנים.
            פעולה זו אינה הפיכה.
          </p>
          <Button
            variant="danger"
            onClick={() => setShowDeleteModal(true)}
            icon={<AlertTriangle size={18} />}
          >
            מחק חשבון לצמיתות
          </Button>
        </div>
      </div>
      
      {/* Password Change Modal */}
      <Modal
        isOpen={showPasswordModal}
        onClose={() => {
          setShowPasswordModal(false);
          passwordForm.reset();
        }}
        title="שינוי סיסמה"
        size="md"
      >
        <form onSubmit={passwordForm.handleSubmit(handlePasswordChange)} className="space-y-4">
          <Input
            label="סיסמה נוכחית"
            type="password"
            required
            {...passwordForm.register('currentPassword', { required: true })}
            error={passwordForm.formState.errors.currentPassword?.message}
          />
          
          <Input
            label="סיסמה חדשה"
            type="password"
            required
            helperText="לפחות 8 תווים, כולל אותיות גדולות וקטנות, מספרים ותווים מיוחדים"
            {...passwordForm.register('newPassword', {
              required: true,
              minLength: { value: 8, message: 'הסיסמה חייבת להכיל לפחות 8 תווים' },
              pattern: {
                value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
                message: 'הסיסמה חייבת להכיל אות גדולה, קטנה, מספר ותו מיוחד'
              }
            })}
            error={passwordForm.formState.errors.newPassword?.message}
          />
          
          <Input
            label="אימות סיסמה חדשה"
            type="password"
            required
            {...passwordForm.register('confirmPassword', { required: true })}
            error={passwordForm.formState.errors.confirmPassword?.message}
          />
          
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={() => {
                setShowPasswordModal(false);
                passwordForm.reset();
              }}
            >
              ביטול
            </Button>
            <Button
              type="submit"
              variant="primary"
              fullWidth
              loading={loading}
            >
              שמור סיסמה חדשה
            </Button>
          </div>
        </form>
      </Modal>
      
      {/* Delete Account Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="אישור מחיקת חשבון"
        size="md"
      >
        <div className="space-y-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertTriangle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
              <div className="space-y-2">
                <h4 className="font-semibold text-red-900">אזהרה: פעולה זו אינה הפיכה!</h4>
                <p className="text-sm text-red-700">
                  כל הנתונים שלך יימחקו לצמיתות, כולל:
                </p>
                <ul className="text-sm text-red-700 space-y-1 mr-4">
                  <li>• כל הקבלות והקבצים המאוחסנים</li>
                  <li>• היסטוריית העריכות</li>
                  <li>• סטטיסטיקות ודוחות</li>
                  <li>• פרטי החשבון והמנוי</li>
                </ul>
              </div>
            </div>
          </div>
          
          <div className="text-center">
            <p className="text-gray-900 font-medium mb-2">
              האם אתה בטוח שברצונך למחוק את החשבון שלך?
            </p>
            <p className="text-sm text-gray-600">
              פעולה זו תמחק את כל הנתונים ולא ניתן יהיה לשחזרם.
            </p>
          </div>
          
          <div className="flex gap-3">
            <Button
              variant="secondary"
              fullWidth
              onClick={() => setShowDeleteModal(false)}
            >
              ביטול
            </Button>
            <Button
              variant="danger"
              fullWidth
              loading={loading}
              onClick={handleAccountDelete}
            >
              כן, מחק את החשבון שלי
            </Button>
          </div>
        </div>
      </Modal>
    </PageContainer>
  );
};

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

/**
 * Tab Button Component
 */
const TabButton: React.FC<{
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}> = ({ active, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className={cn(
      'flex-1 flex items-center justify-center gap-2 px-6 py-4 text-sm font-medium transition-colors',
      'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
      active
        ? 'bg-white text-primary-600 border-b-2 border-primary-600'
        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
    )}
    role="tab"
    aria-selected={active}
  >
    {icon}
    <span>{label}</span>
  </button>
);

/**
 * Profile Tab Component
 */
const ProfileTab: React.FC<{
  form: any;
  onSubmit: (data: ProfileFormData) => void;
  loading: boolean;
  user: any;
}> = ({ form, onSubmit, loading, user }) => (
  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">פרטים אישיים</h3>
      <div className="space-y-4">
        <div className="grid md:grid-cols-2 gap-4">
          <Input
            label="שם מלא"
            required
            icon={<User size={18} />}
            {...form.register('fullName', { 
              required: 'שם מלא הוא שדה חובה',
              minLength: { value: 2, message: 'שם מלא חייב להכיל לפחות 2 תווים' }
            })}
            error={form.formState.errors.fullName?.message}
          />
          
          <Input
            label="טלפון"
            type="tel"
            required
            icon={<Phone size={18} />}
            placeholder="05X-XXX-XXXX"
            {...form.register('phone', {
              required: 'מספר טלפון הוא שדה חובה',
              pattern: {
                value: /^(05\d{8}|05\d-\d{7})$/,
                message: 'מספר טלפון לא תקין (דוגמה: 050-1234567)'
              }
            })}
            error={form.formState.errors.phone?.message}
          />
        </div>
        
        <Input
          label="אימייל"
          type="email"
          disabled
          value={user?.email}
          icon={<Mail size={18} />}
          helperText="לא ניתן לשנות כתובת אימייל"
        />
      </div>
    </div>
    
    <div className="border-t pt-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">פרטי עסק</h3>
      <div className="space-y-4">
        <Input
          label="שם העסק"
          required
          icon={<Building size={18} />}
          {...form.register('businessName', {
            required: 'שם העסק הוא שדה חובה'
          })}
          error={form.formState.errors.businessName?.message}
        />
        
        <Input
          label="מספר עוסק / ח.פ"
          required
          placeholder="12345678 או 123456789"
          {...form.register('businessNumber', {
            required: 'מספר עוסק הוא שדה חובה',
            pattern: {
              value: /^\d{8,9}$/,
              message: 'מספר עוסק חייב להכיל 8-9 ספרות'
            }
          })}
          error={form.formState.errors.businessNumber?.message}
          helperText="8-9 ספרות ללא תווים מיוחדים"
        />
      </div>
    </div>
    
    <div className="flex justify-end pt-4">
      <Button
        type="submit"
        variant="primary"
        loading={loading}
        icon={<CheckCircle size={18} />}
      >
        שמור שינויים
      </Button>
    </div>
  </form>
);

/**
 * Security Tab Component
 */
const SecurityTab: React.FC<{
  onPasswordChange: () => void;
  onLogout: () => void;
  user: any;
}> = ({ onPasswordChange, onLogout, user }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">אבטחה והזדהות</h3>
    </div>
    
    {/* Password Section */}
    <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
      <div className="flex items-start gap-3">
        <Lock className="text-gray-600 mt-0.5" size={20} />
        <div>
          <h4 className="font-medium text-gray-900">סיסמה</h4>
          <p className="text-sm text-gray-600 mt-1">
            שינוי סיסמה אחרון: לפני 30 ימים
          </p>
        </div>
      </div>
      <Button
        variant="secondary"
        onClick={onPasswordChange}
        size="sm"
      >
        שנה סיסמה
      </Button>
    </div>
    
    {/* Phone Verification */}
    <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
      <div className="flex items-start gap-3">
        <Phone className="text-gray-600 mt-0.5" size={20} />
        <div>
          <h4 className="font-medium text-gray-900">אימות טלפון</h4>
          <div className="mt-1">
            {user?.phoneVerified ? (
              <span className="inline-flex items-center gap-1 text-sm text-success-600">
                <CheckCircle size={16} />
                מאומת
              </span>
            ) : (
              <span className="text-sm text-warning-600">לא מאומת</span>
            )}
          </div>
        </div>
      </div>
      {!user?.phoneVerified && (
        <Button
          variant="secondary"
          size="sm"
        >
          אמת עכשיו
        </Button>
      )}
    </div>
    
    {/* Email Verification */}
    <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
      <div className="flex items-start gap-3">
        <Mail className="text-gray-600 mt-0.5" size={20} />
        <div>
          <h4 className="font-medium text-gray-900">אימות אימייל</h4>
          <div className="mt-1">
            {user?.emailVerified ? (
              <span className="inline-flex items-center gap-1 text-sm text-success-600">
                <CheckCircle size={16} />
                מאומת
              </span>
            ) : (
              <span className="text-sm text-warning-600">לא מאומת</span>
            )}
          </div>
        </div>
      </div>
    </div>
    
    {/* Active Sessions */}
    <div className="border-t pt-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">התחברות פעילה</h3>
      <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
        <div className="flex items-start gap-3">
          <Shield className="text-primary-600 mt-0.5" size={20} />
          <div>
            <h4 className="font-medium text-gray-900">מכשיר נוכחי</h4>
            <p className="text-sm text-gray-600 mt-1">
              התחברת לאחרונה: היום בשעה {new Date().getHours()}:{String(new Date().getMinutes()).padStart(2, '0')}
            </p>
          </div>
        </div>
        <Button
          variant="secondary"
          onClick={onLogout}
          icon={<LogOut size={18} />}
          size="sm"
        >
          התנתק
        </Button>
      </div>
    </div>
  </div>
);

/**
 * Subscription Tab Component
 */
const SubscriptionTab: React.FC<{ 
  user: any;
  usagePercentage: number;
  remainingReceipts: number;
}> = ({ user, usagePercentage, remainingReceipts }) => {
  const planNames = {
    free: 'תוכנית חינמית',
    basic: 'Basic',
    pro: 'Pro',
    business: 'Business'
  };
  
  const planColors = {
    free: 'bg-gray-100 text-gray-900',
    basic: 'bg-blue-100 text-blue-900',
    pro: 'bg-purple-100 text-purple-900',
    business: 'bg-gold-100 text-gold-900'
  };
  
  const currentPlan = user?.subscriptionPlan || 'free';
  
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">מנוי ותשלום</h3>
      </div>
      
      {/* Current Plan */}
      <div className="bg-gradient-to-br from-primary-50 to-primary-100 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className={cn(
              'inline-block px-3 py-1 rounded-full text-sm font-semibold',
              planColors[currentPlan as keyof typeof planColors]
            )}>
              {planNames[currentPlan as keyof typeof planNames]}
            </span>
            <p className="text-2xl font-bold text-gray-900 mt-2">
              {currentPlan === 'free' ? 'חינם' : `₪${user?.subscriptionPrice || 0}/חודש`}
            </p>
          </div>
          <Button
            variant="primary"
            size="sm"
          >
            שדרג תוכנית
          </Button>
        </div>
        
        {/* Usage Bar */}
        <div className="mt-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">שימוש חודשי</span>
            <span className="text-sm text-gray-600">
              {user?.receiptsUsedThisMonth || 0} / {user?.receiptsLimit || 10} קבלות
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div
              className={cn(
                'h-2 rounded-full transition-all duration-300',
                usagePercentage >= 100 ? 'bg-red-500' :
                usagePercentage >= 80 ? 'bg-warning-500' :
                'bg-primary-600'
              )}
              style={{
                width: `${Math.min(usagePercentage, 100)}%`
              }}
            />
          </div>
          {usagePercentage >= 80 && (
            <p className="text-sm text-warning-700 mt-2">
              {usagePercentage >= 100 
                ? 'הגעת למכסה החודשית. שדרג לתוכנית גבוהה יותר להמשך שימוש.'
                : `נותרו ${remainingReceipts} קבלות בלבד עד סוף החודש.`
              }
            </p>
          )}
        </div>
      </div>
      
      {/* Plan Features */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-3">היתרונות שלך</h4>
        <ul className="space-y-2">
          <li className="flex items-center gap-2 text-sm text-gray-700">
            <CheckCircle className="text-success-600" size={16} />
            <span>{user?.receiptsLimit || 10} קבלות בחודש</span>
          </li>
          <li className="flex items-center gap-2 text-sm text-gray-700">
            <CheckCircle className="text-success-600" size={16} />
            <span>אחסון מאובטח בענן</span>
          </li>
          <li className="flex items-center gap-2 text-sm text-gray-700">
            <CheckCircle className="text-success-600" size={16} />
            <span>OCR חכם בעברית</span>
          </li>
          {currentPlan !== 'free' && (
            <>
              <li className="flex items-center gap-2 text-sm text-gray-700">
                <CheckCircle className="text-success-600" size={16} />
                <span>ייצוא לאקסל ו-PDF</span>
              </li>
              <li className="flex items-center gap-2 text-sm text-gray-700">
                <CheckCircle className="text-success-600" size={16} />
                <span>תמיכה מועדפת</span>
              </li>
            </>
          )}
        </ul>
      </div>
      
      {/* Billing History */}
      <div>
        <h4 className="font-semibold text-gray-900 mb-3">היסטוריית חיובים</h4>
        <div className="bg-gray-50 rounded-lg p-8 text-center">
          <CreditCard className="mx-auto text-gray-400 mb-3" size={48} />
          <p className="text-gray-600">אין חיובים קודמים</p>
          <p className="text-sm text-gray-500 mt-1">
            {currentPlan === 'free' 
              ? 'עבור לתוכנית בתשלום לצפייה בחיובים'
              : 'החיובים שלך יופיעו כאן'
            }
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
