import React, { useState } from 'react';
import { Image as ImageIcon } from 'lucide-react';

interface ImageLoaderProps {
  src: string;
  alt: string;
  className?: string;
  aspectRatio?: string;
}

export const ImageLoader: React.FC<ImageLoaderProps> = ({ 
  src, 
  alt, 
  className = '',
  aspectRatio = '16/9'
}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  return (
    <div 
      className={`relative bg-gray-100 rounded-lg overflow-hidden ${className}`}
      style={{ aspectRatio }}
    >
      {/* Loading Skeleton */}
      {loading && !error && (
        <div className="absolute inset-0 flex items-center justify-center animate-pulse">
          <ImageIcon className="w-12 h-12 text-gray-400" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
          <ImageIcon className="w-12 h-12 mb-2" />
          <p className="text-sm">שגיאה בטעינת תמונה</p>
        </div>
      )}

      {/* Actual Image */}
      {!error && (
        <img
          src={src}
          alt={alt}
          className={`w-full h-full object-cover transition-opacity duration-300 ${
            loading ? 'opacity-0' : 'opacity-100'
          }`}
          onLoad={() => setLoading(false)}
          onError={() => {
            setLoading(false);
            setError(true);
          }}
          loading="lazy"
        />
      )}
    </div>
  );
};
