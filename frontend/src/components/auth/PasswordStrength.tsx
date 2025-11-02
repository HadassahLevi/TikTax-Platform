import React, { useMemo } from 'react';
import { Check, X } from 'lucide-react';

interface PasswordStrengthProps {
  password: string;
  showRequirements?: boolean;
}

interface PasswordRequirement {
  label: string;
  test: (password: string) => boolean;
}

/**
 * Password Strength Indicator Component
 * 
 * Displays:
 * - Visual strength bar (weak/medium/strong)
 * - Checklist of password requirements
 * - Real-time validation feedback
 * 
 * @component
 * @example
 * ```tsx
 * <PasswordStrength
 *   password={passwordValue}
 *   showRequirements={true}
 * />
 * ```
 */
export const PasswordStrength: React.FC<PasswordStrengthProps> = ({
  password,
  showRequirements = true
}) => {
  // Define password requirements
  const requirements: PasswordRequirement[] = useMemo(
    () => [
      {
        label: 'לפחות 8 תווים',
        test: (pwd: string) => pwd.length >= 8
      },
      {
        label: 'אות גדולה באנגלית',
        test: (pwd: string) => /[A-Z]/.test(pwd)
      },
      {
        label: 'אות קטנה באנגלית',
        test: (pwd: string) => /[a-z]/.test(pwd)
      },
      {
        label: 'לפחות ספרה אחת',
        test: (pwd: string) => /[0-9]/.test(pwd)
      }
    ],
    []
  );

  // Calculate password strength
  const strength = useMemo(() => {
    if (!password) return 0;

    const passedRequirements = requirements.filter(req => req.test(password)).length;
    const percentage = (passedRequirements / requirements.length) * 100;

    if (percentage < 50) return 1; // Weak
    if (percentage < 100) return 2; // Medium
    return 3; // Strong
  }, [password, requirements]);

  // Get strength label and color
  const getStrengthInfo = () => {
    switch (strength) {
      case 1:
        return {
          label: 'חלשה',
          color: 'bg-red-500',
          textColor: 'text-red-600',
          width: 'w-1/3'
        };
      case 2:
        return {
          label: 'בינונית',
          color: 'bg-yellow-500',
          textColor: 'text-yellow-600',
          width: 'w-2/3'
        };
      case 3:
        return {
          label: 'חזקה',
          color: 'bg-green-500',
          textColor: 'text-green-600',
          width: 'w-full'
        };
      default:
        return {
          label: '',
          color: 'bg-gray-300',
          textColor: 'text-gray-400',
          width: 'w-0'
        };
    }
  };

  const strengthInfo = getStrengthInfo();

  if (!password) return null;

  return (
    <div className="space-y-3">
      {/* Strength bar */}
      <div>
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-gray-600">חוזק סיסמה:</span>
          {strength > 0 && (
            <span className={`text-xs font-semibold ${strengthInfo.textColor}`}>
              {strengthInfo.label}
            </span>
          )}
        </div>
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full ${strengthInfo.color} transition-all duration-300 ${strengthInfo.width}`}
          />
        </div>
      </div>

      {/* Requirements checklist */}
      {showRequirements && (
        <div className="space-y-1">
          <p className="text-xs font-medium text-gray-600 mb-2">הסיסמה חייבת לכלול:</p>
          {requirements.map((req, index) => {
            const isPassed = req.test(password);
            return (
              <div
                key={index}
                className="flex items-center gap-2 text-xs"
              >
                {isPassed ? (
                  <Check className="w-4 h-4 text-green-500 flex-shrink-0" />
                ) : (
                  <X className="w-4 h-4 text-gray-300 flex-shrink-0" />
                )}
                <span
                  className={`
                    ${isPassed ? 'text-green-600' : 'text-gray-500'}
                  `}
                >
                  {req.label}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default PasswordStrength;
