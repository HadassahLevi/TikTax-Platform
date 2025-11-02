import React from 'react';

interface ProgressIndicatorProps {
  currentStep: number;
  totalSteps: number;
  labels?: string[];
}

/**
 * Progress Indicator Component
 * 
 * Shows current progress through multi-step form with:
 * - Filled circles for completed steps (green)
 * - Filled circle for current step (blue)
 * - Hollow circles for upcoming steps (gray)
 * - Animated lines between steps
 * 
 * @component
 * @example
 * ```tsx
 * <ProgressIndicator
 *   currentStep={2}
 *   totalSteps={3}
 *   labels={['פרטים אישיים', 'פרטי עסק', 'אימות']}
 * />
 * ```
 */
export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({
  currentStep,
  totalSteps,
  labels = []
}) => {
  return (
    <div className="w-full mb-8">
      {/* Progress bar */}
      <div className="relative flex items-center justify-between">
        {Array.from({ length: totalSteps }).map((_, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;
          const isUpcoming = stepNumber > currentStep;

          return (
            <React.Fragment key={stepNumber}>
              {/* Step circle */}
              <div className="relative z-10 flex flex-col items-center">
                <div
                  className={`
                    flex items-center justify-center
                    w-10 h-10 rounded-full border-2 transition-all duration-300
                    ${isCompleted ? 'bg-green-500 border-green-500' : ''}
                    ${isCurrent ? 'bg-primary border-primary' : ''}
                    ${isUpcoming ? 'bg-white border-gray-300' : ''}
                  `}
                >
                  {isCompleted && (
                    <svg
                      className="w-5 h-5 text-white"
                      fill="none"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M5 13l4 4L19 7"></path>
                    </svg>
                  )}
                  {!isCompleted && (
                    <span
                      className={`
                        text-sm font-semibold
                        ${isCurrent ? 'text-white' : 'text-gray-400'}
                      `}
                    >
                      {stepNumber}
                    </span>
                  )}
                </div>

                {/* Step label (optional) */}
                {labels[index] && (
                  <span
                    className={`
                      mt-2 text-xs font-medium text-center
                      ${isCurrent ? 'text-primary' : ''}
                      ${isCompleted ? 'text-green-600' : ''}
                      ${isUpcoming ? 'text-gray-400' : ''}
                    `}
                  >
                    {labels[index]}
                  </span>
                )}
              </div>

              {/* Connecting line */}
              {index < totalSteps - 1 && (
                <div className="relative flex-1 h-0.5 mx-2">
                  {/* Background line (gray) */}
                  <div className="absolute inset-0 bg-gray-300 rounded"></div>

                  {/* Progress line (colored) */}
                  <div
                    className={`
                      absolute inset-0 rounded transition-all duration-400
                      ${stepNumber < currentStep ? 'bg-green-500 scale-x-100' : 'bg-gray-300 scale-x-0'}
                    `}
                    style={{ transformOrigin: 'right' }}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Mobile-friendly step text */}
      <div className="mt-4 text-center md:hidden">
        <p className="text-sm text-gray-600">
          שלב {currentStep} מתוך {totalSteps}
        </p>
      </div>
    </div>
  );
};

export default ProgressIndicator;
