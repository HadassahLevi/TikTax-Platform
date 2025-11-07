import React from 'react';
import { SkeletonCard } from './SkeletonCard';

interface SkeletonListProps {
  count?: number;
  variant?: 'stat' | 'receipt' | 'default';
  className?: string;
}

export const SkeletonList: React.FC<SkeletonListProps> = ({ 
  count = 3, 
  variant = 'default',
  className = ''
}) => {
  return (
    <div className={className}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} variant={variant} />
      ))}
    </div>
  );
};
