import React, { useState } from 'react';
import Input from './Input';
import { Mail, Phone, User, Lock, Calendar, Search } from 'lucide-react';

/**
 * Input Component Demo
 * 
 * Showcases all Input component variants, states, and features.
 * This file demonstrates proper usage patterns for the Input component.
 */
const InputDemo: React.FC = () => {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState('');
  const [password, setPassword] = useState('');
  const [description, setDescription] = useState('');
  const [validEmail, setValidEmail] = useState('user@example.com');

  // Email validation
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    
    if (value && !value.includes('@')) {
      setEmailError('כתובת דוא״ל לא תקינה');
    } else {
      setEmailError('');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8" dir="rtl">
      <div className="mx-auto max-w-4xl space-y-12">
        
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Input Component Demo</h1>
          <p className="mt-2 text-gray-600">כל המצבים והווריאציות של רכיב ה-Input</p>
        </div>

        {/* Basic Inputs */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">1. Basic Inputs</h2>
          
          <div className="grid gap-6 md:grid-cols-2">
            <Input
              label="שם מלא"
              placeholder="הזן שם מלא"
              type="text"
            />
            
            <Input
              label="שם מלא (חובה)"
              placeholder="הזן שם מלא"
              type="text"
              required
            />
            
            <Input
              label="דוא״ל"
              placeholder="example@tiktax.co.il"
              type="email"
            />
            
            <Input
              label="טלפון"
              placeholder="050-1234567"
              type="tel"
            />
            
            <Input
              label="תאריך"
              type="date"
            />
            
            <Input
              label="כתובת URL"
              placeholder="https://example.com"
              type="url"
            />
          </div>
        </section>

        {/* Validation States */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">2. Validation States</h2>
          
          <div className="grid gap-6 md:grid-cols-2">
            {/* Default */}
            <Input
              label="מצב רגיל"
              placeholder="הזן טקסט"
              type="text"
            />
            
            {/* Error */}
            <Input
              label="שגיאה"
              placeholder="הזן דוא״ל"
              type="email"
              value={email}
              onChange={handleEmailChange}
              error={emailError}
            />
            
            {/* Success */}
            <Input
              label="הצלחה"
              placeholder="example@tiktax.co.il"
              type="email"
              value={validEmail}
              onChange={(e) => setValidEmail(e.target.value)}
              success
            />
            
            {/* Disabled */}
            <Input
              label="מושבת"
              placeholder="לא ניתן לערוך"
              type="text"
              disabled
              value="ערך קבוע"
            />
          </div>
        </section>

        {/* Password Input */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">3. Password Input</h2>
          
          <div className="grid gap-6 md:grid-cols-2">
            <Input
              label="סיסמה"
              type="password"
              placeholder="הזן סיסמה"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              helperText="לפחות 8 תווים"
              required
            />
            
            <Input
              label="אימות סיסמה"
              type="password"
              placeholder="הזן סיסמה שוב"
              required
            />
            
            <Input
              label="סיסמה עם שגיאה"
              type="password"
              placeholder="הזן סיסמה"
              error="הסיסמה חייבת להכיל לפחות 8 תווים"
            />
            
            <Input
              label="סיסמה תקינה"
              type="password"
              value="SecurePass123!"
              success
            />
          </div>
        </section>

        {/* With Icons */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">4. With Icons</h2>
          
          <div className="grid gap-6 md:grid-cols-2">
            <Input
              label="דוא״ל עם אייקון"
              placeholder="example@tiktax.co.il"
              type="email"
              icon={<Mail size={20} />}
              iconPosition="right"
            />
            
            <Input
              label="טלפון עם אייקון"
              placeholder="050-1234567"
              type="tel"
              icon={<Phone size={20} />}
              iconPosition="right"
            />
            
            <Input
              label="שם משתמש"
              placeholder="הזן שם משתמש"
              type="text"
              icon={<User size={20} />}
              iconPosition="left"
            />
            
            <Input
              label="חיפוש"
              placeholder="חפש..."
              type="text"
              icon={<Search size={20} />}
              iconPosition="right"
            />
          </div>
        </section>

        {/* Helper Text & Character Counter */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">5. Helper Text & Character Counter</h2>
          
          <div className="space-y-6">
            <Input
              label="תיאור קצר"
              placeholder="הזן תיאור (עד 50 תווים)"
              type="text"
              helperText="תיאור קצר לקבלה (אופציונלי)"
              maxLength={50}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            
            <Input
              label="הערות"
              placeholder="הזן הערות נוספות"
              type="text"
              helperText="ניתן להוסיף הערות נוספות לקבלה"
            />
            
            <Input
              label="שם עסק"
              placeholder="הזן שם עסק"
              type="text"
              maxLength={100}
              value="שם עסק ארוך מאוד שעובר את המגבלה"
            />
          </div>
        </section>

        {/* Full Width */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">6. Full Width</h2>
          
          <Input
            label="כתובת מלאה"
            placeholder="הזן כתובת מלאה"
            type="text"
            fullWidth
            helperText="רחוב, מספר בית, עיר, מיקוד"
          />
          
          <Input
            label="הערות ארוכות"
            placeholder="הזן הערות מפורטות..."
            type="text"
            fullWidth
            maxLength={200}
            value=""
          />
        </section>

        {/* Real-World Form Example */}
        <section className="space-y-6 rounded-xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-gray-900">7. Real-World Form Example</h2>
          
          <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
            <Input
              label="שם מלא"
              placeholder="הזן שם מלא"
              type="text"
              icon={<User size={20} />}
              iconPosition="right"
              required
            />
            
            <Input
              label="דוא״ל"
              placeholder="example@tiktax.co.il"
              type="email"
              icon={<Mail size={20} />}
              iconPosition="right"
              required
            />
            
            <Input
              label="טלפון נייד"
              placeholder="050-1234567"
              type="tel"
              icon={<Phone size={20} />}
              iconPosition="right"
              helperText="מספר הטלפון ישמש לאימות חשבון"
              required
            />
            
            <Input
              label="סיסמה"
              type="password"
              placeholder="לפחות 8 תווים"
              icon={<Lock size={20} />}
              iconPosition="right"
              helperText="השתמש באותיות, מספרים ותווים מיוחדים"
              required
            />
            
            <Input
              label="תאריך לידה"
              type="date"
              icon={<Calendar size={20} />}
              iconPosition="right"
            />
            
            <button
              type="submit"
              className="w-full rounded-lg bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
            >
              שמור פרטים
            </button>
          </form>
        </section>

        {/* Accessibility Features */}
        <section className="space-y-4 rounded-xl bg-blue-50 p-6">
          <h2 className="text-xl font-semibold text-gray-900">♿ Accessibility Features</h2>
          <ul className="space-y-2 text-sm text-gray-700">
            <li>✓ Proper label association with htmlFor</li>
            <li>✓ ARIA attributes (aria-invalid, aria-describedby)</li>
            <li>✓ Error announcements for screen readers</li>
            <li>✓ Keyboard navigation support</li>
            <li>✓ Focus visible indicators</li>
            <li>✓ Required field indicators with aria-label</li>
            <li>✓ Password toggle with proper aria-label</li>
            <li>✓ Disabled state with proper cursor and colors</li>
          </ul>
        </section>

      </div>
    </div>
  );
};

export default InputDemo;
