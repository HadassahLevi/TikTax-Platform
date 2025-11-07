import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  progress: number; // 0-100
  label?: string;
  showPercentage?: boolean;
  color?: 'primary' | 'success' | 'warning' | 'danger';
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ 
  progress,
  label,
  showPercentage = true,
  color = 'primary'
}) => {
  const colorClasses = {
    primary: '#2563EB',
    success: '#059669',
    warning: '#F59E0B',
    danger: '#EF4444'
  };

  return (
    <div className="space-y-2">
      {(label || showPercentage) && (
        <div className="flex items-center justify-between text-sm">
          {label && <span className="text-gray-700">{label}</span>}
          {showPercentage && (
            <span className="text-gray-600 font-medium">{Math.round(progress)}%</span>
          )}
        </div>
      )}
      
      <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
          style={{ 
            height: '100%',
            backgroundColor: colorClasses[color],
            borderRadius: '9999px'
          }}
        />
      </div>
    </div>
  );
};
