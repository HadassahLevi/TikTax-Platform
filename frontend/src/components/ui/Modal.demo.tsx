/**
 * Modal Component Demo
 * 
 * Comprehensive examples demonstrating all Modal features:
 * - Size variants
 * - Accessibility features
 * - Form integration
 * - Confirmation dialogs
 * - Multi-step workflows
 * - Loading states
 * 
 * Usage: Import this file into your development environment to see live examples
 */

import { useState } from 'react';
import Modal, { useModal } from './Modal';
import Button from './Button';
import Input from './Input';
import { 
  Plus, 
  Trash2, 
  Settings, 
  HelpCircle, 
  Upload,
  AlertTriangle,
  CheckCircle,
  Loader2 
} from 'lucide-react';

// ============================================================================
// DEMO 1: Basic Modal
// ============================================================================
export const BasicModalDemo = () => {
  const { isOpen, open, close } = useModal();

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 1: חלון בסיסי</h3>
      
      <Button onClick={open}>פתח חלון בסיסי</Button>

      <Modal isOpen={isOpen} onClose={close} title="חלון בסיסי">
        <div className="space-y-4">
          <p className="text-gray-600">
            זהו חלון בסיסי עם כותרת ותוכן פשוט.
          </p>
          <p className="text-gray-600">
            אתה יכול לסגור אותו על ידי:
          </p>
          <ul className="list-disc list-inside text-gray-600 space-y-2">
            <li>לחיצה על כפתור ה-X</li>
            <li>לחיצה על הרקע</li>
            <li>לחיצה על מקש ESC</li>
          </ul>
        </div>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 2: Size Variants
// ============================================================================
export const SizeVariantsDemo = () => {
  const sm = useModal();
  const md = useModal();
  const lg = useModal();
  const xl = useModal();
  const full = useModal();

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 2: גדלי חלונות</h3>
      
      <div className="flex flex-wrap gap-3">
        <Button size="sm" onClick={sm.open}>קטן (sm)</Button>
        <Button size="sm" onClick={md.open}>בינוני (md)</Button>
        <Button size="sm" onClick={lg.open}>גדול (lg)</Button>
        <Button size="sm" onClick={xl.open}>גדול מאוד (xl)</Button>
        <Button size="sm" onClick={full.open}>מלא (full)</Button>
      </div>

      <Modal isOpen={sm.isOpen} onClose={sm.close} title="חלון קטן" size="sm">
        <p>מקסימום רוחב: 400px</p>
        <p className="text-sm text-gray-500 mt-2">מושלם לאישורים פשוטים</p>
      </Modal>

      <Modal isOpen={md.isOpen} onClose={md.close} title="חלון בינוני" size="md">
        <p>מקסימום רוחב: 600px (ברירת מחדל)</p>
        <p className="text-sm text-gray-500 mt-2">מתאים לרוב המקרים</p>
      </Modal>

      <Modal isOpen={lg.isOpen} onClose={lg.close} title="חלון גדול" size="lg">
        <p>מקסימום רוחב: 800px</p>
        <p className="text-sm text-gray-500 mt-2">טפסים מורכבים או טבלאות</p>
      </Modal>

      <Modal isOpen={xl.isOpen} onClose={xl.close} title="חלון גדול מאוד" size="xl">
        <p>מקסימום רוחב: 1200px</p>
        <p className="text-sm text-gray-500 mt-2">תוכן עשיר, דשבורדים</p>
      </Modal>

      <Modal isOpen={full.isOpen} onClose={full.close} title="חלון מלא" size="full">
        <p>מקסימום רוחב: 95vw</p>
        <p className="text-sm text-gray-500 mt-2">חוויה כמעט מסך מלא</p>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 3: With Footer (Action Buttons)
// ============================================================================
export const WithFooterDemo = () => {
  const { isOpen, open, close } = useModal();
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => {
      close();
      setSaved(false);
    }, 1500);
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 3: חלון עם כפתורי פעולה</h3>
      
      <Button onClick={open} icon={<Settings />}>הגדרות</Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="הגדרות חשבון"
        footer={
          <div className="flex gap-3 justify-end">
            <Button variant="secondary" onClick={close} disabled={saved}>
              ביטול
            </Button>
            <Button 
              variant="primary" 
              onClick={handleSave}
              loading={saved}
              icon={saved ? <CheckCircle size={16} /> : undefined}
            >
              {saved ? 'נשמר!' : 'שמור שינויים'}
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <Input label="שם מלא" defaultValue="דוד כהן" />
          <Input label="אימייל" type="email" defaultValue="david@example.com" />
          <Input label="טלפון" type="tel" defaultValue="050-1234567" />
        </div>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 4: Confirmation Dialog
// ============================================================================
export const ConfirmationDemo = () => {
  const { isOpen, open, close } = useModal();
  const [deleted, setDeleted] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDelete = () => {
    setDeleting(true);
    
    // Simulate API call
    setTimeout(() => {
      setDeleting(false);
      setDeleted(true);
      
      setTimeout(() => {
        close();
        setDeleted(false);
      }, 1500);
    }, 1000);
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 4: חלון אישור</h3>
      
      <Button variant="danger" icon={<Trash2 />} onClick={open}>
        מחק קבלה
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="אישור מחיקה"
        size="sm"
        closeOnOverlayClick={!deleting}
        closeOnEsc={!deleting}
        footer={
          <div className="flex gap-3 justify-end">
            <Button 
              variant="secondary" 
              onClick={close}
              disabled={deleting || deleted}
            >
              ביטול
            </Button>
            <Button 
              variant="danger" 
              onClick={handleDelete}
              loading={deleting}
              disabled={deleted}
              icon={deleted ? <CheckCircle size={16} /> : <Trash2 size={16} />}
            >
              {deleted ? 'נמחק!' : deleting ? 'מוחק...' : 'מחק'}
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="text-red-500 flex-shrink-0 mt-1" size={20} />
            <div className="space-y-2">
              <p className="text-gray-900 font-medium">
                האם אתה בטוח שברצונך למחוק את הקבלה?
              </p>
              <p className="text-sm text-gray-600">
                קבלה: <strong>סופר דוד - ₪450.00</strong>
              </p>
              <p className="text-sm text-red-600">
                פעולה זו אינה ניתנת לביטול.
              </p>
            </div>
          </div>
        </div>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 5: Form Modal with Validation
// ============================================================================
export const FormModalDemo = () => {
  const { isOpen, open, close } = useModal();
  const [formData, setFormData] = useState({
    business: '',
    amount: '',
    date: new Date().toISOString().split('T')[0],
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.business.trim()) {
      newErrors.business = 'שדה חובה';
    }
    
    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'הכנס סכום תקין';
    }
    
    if (!formData.date) {
      newErrors.date = 'שדה חובה';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (!validateForm()) return;

    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      close();
      
      // Reset form
      setFormData({
        business: '',
        amount: '',
        date: new Date().toISOString().split('T')[0],
      });
      setErrors({});
    }, 1500);
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 5: טופס עם ולידציה</h3>
      
      <Button onClick={open} icon={<Plus />}>הוסף קבלה ידנית</Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="הוסף קבלה חדשה"
        size="md"
        closeOnOverlayClick={false} // Prevent accidental close
        footer={
          <div className="flex gap-3 justify-end">
            <Button 
              variant="secondary" 
              onClick={close}
              disabled={loading}
            >
              ביטול
            </Button>
            <Button 
              variant="primary" 
              onClick={handleSubmit}
              loading={loading}
            >
              שמור
            </Button>
          </div>
        }
      >
        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <Input
            label="שם עסק"
            value={formData.business}
            onChange={(e) => handleChange('business', e.target.value)}
            error={errors.business}
            placeholder="לדוגמה: סופר דוד"
          />
          
          <Input
            label="סכום"
            type="number"
            value={formData.amount}
            onChange={(e) => handleChange('amount', e.target.value)}
            error={errors.amount}
            placeholder="0.00"
            helperText="סכום בשקלים"
          />

          <Input
            label="תאריך"
            type="date"
            value={formData.date}
            onChange={(e) => handleChange('date', e.target.value)}
            error={errors.date}
          />
        </form>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 6: Multi-Step Modal
// ============================================================================
export const MultiStepDemo = () => {
  const { isOpen, open, close } = useModal();
  const [step, setStep] = useState(1);
  const totalSteps = 3;

  const nextStep = () => setStep(s => Math.min(s + 1, totalSteps));
  const prevStep = () => setStep(s => Math.max(s - 1, 1));
  
  const handleClose = () => {
    close();
    setStep(1); // Reset
  };

  const handleFinish = () => {
    // Process data
    handleClose();
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 6: חלון רב-שלבי</h3>
      
      <Button onClick={open} icon={<Upload />}>העלאת קבלה מונחית</Button>

      <Modal
        isOpen={isOpen}
        onClose={handleClose}
        title={`שלב ${step} מתוך ${totalSteps}: ${
          step === 1 ? 'העלאת תמונה' : 
          step === 2 ? 'אימות נתונים' : 
          'סיכום'
        }`}
        size="lg"
        closeOnEsc={false}
        footer={
          <div className="flex gap-3 justify-between w-full">
            <Button 
              variant="secondary"
              onClick={prevStep}
              disabled={step === 1}
            >
              חזור
            </Button>
            
            <div className="flex gap-2">
              {[1, 2, 3].map(i => (
                <div
                  key={i}
                  className={`w-2 h-2 rounded-full ${
                    i <= step ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>

            <Button
              variant="primary"
              onClick={step === totalSteps ? handleFinish : nextStep}
            >
              {step === totalSteps ? 'סיום' : 'המשך'}
            </Button>
          </div>
        }
      >
        {step === 1 && (
          <div className="space-y-4 text-center py-8">
            <Upload className="mx-auto text-blue-600" size={48} />
            <h4 className="text-lg font-medium">העלה תמונת קבלה</h4>
            <p className="text-gray-600">גרור קובץ או לחץ לבחירה</p>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12">
              <Button variant="secondary">בחר קובץ</Button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4 py-4">
            <p className="text-gray-600 mb-4">אמת את הפרטים שזוהו:</p>
            <Input label="שם עסק" defaultValue="סופר דוד" />
            <Input label="סכום" defaultValue="450.00" />
            <Input label="תאריך" type="date" defaultValue="2024-11-02" />
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4 py-8">
            <div className="flex items-center justify-center gap-3 text-green-600 mb-4">
              <CheckCircle size={32} />
              <h4 className="text-xl font-semibold">הקבלה מוכנה לשמירה</h4>
            </div>
            <div className="bg-gray-50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">עסק:</span>
                <span className="font-medium">סופר דוד</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">סכום:</span>
                <span className="font-medium">₪450.00</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">תאריך:</span>
                <span className="font-medium">02/11/2024</span>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 7: Forced Modal (Cannot Close)
// ============================================================================
export const ForcedModalDemo = () => {
  const { isOpen, open, close } = useModal();
  const [processing, setProcessing] = useState(false);

  const handleStart = () => {
    open();
    setProcessing(true);

    // Simulate long process
    setTimeout(() => {
      setProcessing(false);
    }, 3000);
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 7: חלון מאולץ (לא ניתן לסגירה)</h3>
      
      <Button onClick={handleStart}>התחל עיבוד</Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        closeOnOverlayClick={false}
        closeOnEsc={false}
        showCloseButton={!processing}
        size="sm"
        title={processing ? undefined : "העיבוד הסתיים"}
      >
        <div className="flex flex-col items-center gap-4 py-6">
          {processing ? (
            <>
              <Loader2 className="w-12 h-12 animate-spin text-blue-600" />
              <p className="text-lg font-medium">מעבד קבלה...</p>
              <p className="text-sm text-gray-500">אנא המתן, זה עשוי לקחת מספר שניות</p>
            </>
          ) : (
            <>
              <CheckCircle className="w-12 h-12 text-green-600" />
              <p className="text-lg font-medium">העיבוד הושלם בהצלחה!</p>
              <Button onClick={close} fullWidth>סגור</Button>
            </>
          )}
        </div>
      </Modal>
    </div>
  );
};

// ============================================================================
// DEMO 8: Help/Information Modal
// ============================================================================
export const HelpModalDemo = () => {
  const { isOpen, open, close } = useModal();

  return (
    <div className="p-6 space-y-4">
      <h3 className="text-xl font-semibold">דמו 8: חלון עזרה</h3>
      
      <Button variant="ghost" icon={<HelpCircle />} onClick={open}>
        עזרה
      </Button>

      <Modal
        isOpen={isOpen}
        onClose={close}
        title="מדריך למשתמש"
        size="lg"
      >
        <div className="prose prose-sm max-w-none space-y-4">
          <section>
            <h3 className="text-lg font-semibold text-gray-900">כיצד להשתמש במערכת</h3>
            <p className="text-gray-600">
              ברוכים הבאים למערכת ניהול הקבלות של Tik-Tax. 
              מערכת זו מאפשרת לך לנהל בקלות את כל הקבלות שלך עם טכנולוגיית OCR מתקדמת.
            </p>
          </section>

          <section>
            <h4 className="text-base font-semibold text-gray-900">שלב 1: העלאת קבלה</h4>
            <ul className="list-disc list-inside text-gray-600 space-y-1">
              <li>צלם תמונה של הקבלה באמצעות המצלמה</li>
              <li>או העלה קובץ קיים מהמכשיר שלך</li>
              <li>המערכת תזהה אוטומטית את הפרטים</li>
            </ul>
          </section>

          <section>
            <h4 className="text-base font-semibold text-gray-900">שלב 2: אימות נתונים</h4>
            <ul className="list-disc list-inside text-gray-600 space-y-1">
              <li>בדוק את הפרטים שזוהו</li>
              <li>ערוך במידת הצורך</li>
              <li>בחר קטגוריה מתאימה</li>
            </ul>
          </section>

          <section>
            <h4 className="text-base font-semibold text-gray-900">שלב 3: שמירה וארכיון</h4>
            <ul className="list-disc list-inside text-gray-600 space-y-1">
              <li>שמור את הקבלה במאגר</li>
              <li>הקבלה תישמר בצורה מאובטחת ל-7 שנים</li>
              <li>ניתן לייצא לאקסל בכל עת</li>
            </ul>
          </section>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
            <p className="text-sm text-blue-900">
              <strong>טיפ:</strong> השתמש במקש Tab לניווט בין שדות בטפסים
            </p>
          </div>
        </div>
      </Modal>
    </div>
  );
};

// ============================================================================
// MAIN DEMO SHOWCASE
// ============================================================================
export const ModalDemoShowcase = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Modal Component - Demo Showcase
          </h1>
          <p className="text-xl text-gray-600">
            דוגמאות מקיפות לכל התכונות והאפשרויות
          </p>
        </header>

        <div className="grid gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <BasicModalDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <SizeVariantsDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <WithFooterDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <ConfirmationDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <FormModalDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <MultiStepDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <ForcedModalDemo />
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200">
            <HelpModalDemo />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModalDemoShowcase;
