import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronLeft, Home } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  path: string;
}

// Route label mapping (Hebrew)
const ROUTE_LABELS: Record<string, string> = {
  'dashboard': 'דשבורד',
  'archive': 'ארכיון קבלות',
  'receipts': 'קבלות',
  'upload': 'העלאת קבלה',
  'export': 'ייצוא נתונים',
  'profile': 'פרופיל',
  'settings': 'הגדרות',
  'security': 'אבטחה',
  'subscription': 'מנוי ותמחור',
  'help': 'עזרה ותמיכה',
  'faq': 'שאלות נפוצות',
  'about': 'אודות',
  'privacy': 'מדיניות פרטיות',
  'terms': 'תנאי שימוש'
};

export const Breadcrumbs: React.FC = () => {
  const location = useLocation();
  
  // Split pathname and filter empty strings
  const pathnames = location.pathname.split('/').filter(x => x);

  // Don't show breadcrumbs on home/dashboard only
  if (pathnames.length === 0 || (pathnames.length === 1 && pathnames[0] === 'dashboard')) {
    return null;
  }

  // Build breadcrumb trail
  const breadcrumbs: BreadcrumbItem[] = [
    { label: 'בית', path: '/dashboard' }
  ];

  let currentPath = '';
  pathnames.forEach((segment) => {
    currentPath += `/${segment}`;
    
    // Get label from mapping or use segment as-is
    const label = ROUTE_LABELS[segment] || segment;
    
    // Skip numeric IDs (like /receipts/123)
    if (!/^\d+$/.test(segment)) {
      breadcrumbs.push({ label, path: currentPath });
    }
  });

  return (
    <nav 
      className="flex items-center gap-2 mb-6 text-sm overflow-x-auto scrollbar-hide" 
      aria-label="Breadcrumb"
    >
      {/* Home Icon */}
      <Link
        to="/dashboard"
        className="
          flex items-center gap-1.5 
          text-gray-600 hover:text-primary-600 
          transition-colors 
          flex-shrink-0
          px-2 py-1 rounded
          hover:bg-gray-100
        "
        aria-label="חזור לדף הבית"
      >
        <Home className="w-4 h-4" />
        <span className="hidden sm:inline">בית</span>
      </Link>

      {/* Breadcrumb Trail */}
      {breadcrumbs.slice(1).map((item, index) => {
        const isLast = index === breadcrumbs.length - 2;
        
        return (
          <React.Fragment key={item.path}>
            {/* Separator */}
            <ChevronLeft className="w-4 h-4 text-gray-400 flex-shrink-0" aria-hidden="true" />
            
            {/* Breadcrumb Item */}
            {isLast ? (
              // Current page (not clickable)
              <span 
                className="text-gray-900 font-medium truncate max-w-[200px]"
                aria-current="page"
              >
                {item.label}
              </span>
            ) : (
              // Clickable link
              <Link
                to={item.path}
                className="
                  text-gray-600 hover:text-primary-600 
                  transition-colors 
                  truncate max-w-[200px]
                  px-2 py-1 rounded
                  hover:bg-gray-100
                "
              >
                {item.label}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
