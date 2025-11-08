/**
 * Browser compatibility fixes for TIK-TAX
 * Handles Safari, iOS, Android quirks
 */

/**
 * Detect Safari browser
 */
export const isSafari = (): boolean => {
  return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
};

/**
 * Detect iOS devices
 */
export const isIOS = (): boolean => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) || 
         (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
};

/**
 * Detect Android devices
 */
export const isAndroid = (): boolean => {
  return /Android/.test(navigator.userAgent);
};

/**
 * Detect mobile device (any)
 */
export const isMobile = (): boolean => {
  return isIOS() || isAndroid() || 
         /webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

/**
 * Fix iOS 100vh issue
 * iOS Safari changes viewport height when URL bar shows/hides
 */
export const fixIOSViewportHeight = () => {
  if (!isIOS()) return;

  const setVH = () => {
    // Get actual viewport height
    const vh = window.innerHeight * 0.01;
    // Set CSS custom property
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  };

  // Set on load
  setVH();

  // Update on resize and orientation change
  window.addEventListener('resize', setVH);
  window.addEventListener('orientationchange', () => {
    // Delay for orientation change completion
    setTimeout(setVH, 100);
  });
};

/**
 * Fix iOS input zoom
 * Prevent iOS from zooming when focusing on inputs with font-size < 16px
 */
export const preventIOSInputZoom = () => {
  if (!isIOS()) return;

  // Add viewport meta tag that prevents zoom on input focus
  const viewport = document.querySelector('meta[name=viewport]');
  if (viewport) {
    viewport.setAttribute('content', 
      'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
    );
  }
};

/**
 * Fix Safari date input format
 * Safari requires yyyy-mm-dd format
 */
export const formatDateForSafari = (date: string): string => {
  if (!isSafari()) return date;

  // If date is in dd/mm/yyyy format, convert to yyyy-mm-dd
  const ddmmyyyy = /^(\d{2})\/(\d{2})\/(\d{4})$/;
  const match = date.match(ddmmyyyy);
  
  if (match) {
    const [, day, month, year] = match;
    return `${year}-${month}-${day}`;
  }

  return date;
};

/**
 * Fix iOS Safari safe area insets
 * Handle notch and home indicator on newer iPhones
 */
export const applyIOSSafeAreaInsets = () => {
  if (!isIOS()) return;

  // This is handled in CSS using env() variables
  // Just ensure viewport-fit=cover is set
  const viewport = document.querySelector('meta[name=viewport]');
  if (viewport) {
    const content = viewport.getAttribute('content') || '';
    if (!content.includes('viewport-fit')) {
      viewport.setAttribute('content', `${content}, viewport-fit=cover`);
    }
  }
};

/**
 * Disable pull-to-refresh on mobile
 * Prevents accidental page refresh when scrolling
 */
export const disablePullToRefresh = () => {
  if (!isMobile()) return;

  let lastTouchY = 0;
  let maybePreventPullToRefresh = false;

  document.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 1) return;
    lastTouchY = e.touches[0].clientY;
    maybePreventPullToRefresh = window.pageYOffset === 0;
  }, { passive: false });

  document.addEventListener('touchmove', (e) => {
    const touchY = e.touches[0].clientY;
    const touchYDelta = touchY - lastTouchY;
    lastTouchY = touchY;

    if (maybePreventPullToRefresh && touchYDelta > 0) {
      e.preventDefault();
      return;
    }

    maybePreventPullToRefresh = false;
  }, { passive: false });
};

/**
 * Fix Android keyboard pushing content
 * Handle virtual keyboard showing/hiding
 */
export const handleAndroidKeyboard = () => {
  if (!isAndroid()) return;

  const originalHeight = window.innerHeight;

  window.addEventListener('resize', () => {
    const currentHeight = window.innerHeight;
    
    // If height decreased significantly, keyboard is probably showing
    if (originalHeight - currentHeight > 150) {
      document.body.classList.add('keyboard-open');
    } else {
      document.body.classList.remove('keyboard-open');
    }
  });
};

/**
 * Fix Safari flexbox bugs
 * Safari has known issues with flexbox
 */
export const fixSafariFlexbox = () => {
  if (!isSafari()) return;

  // Add specific Safari class for CSS fixes
  document.documentElement.classList.add('safari');
};

/**
 * Initialize all browser fixes
 * Call this once on app initialization
 */
export const initBrowserFixes = () => {
  fixIOSViewportHeight();
  applyIOSSafeAreaInsets();
  disablePullToRefresh();
  handleAndroidKeyboard();
  fixSafariFlexbox();

  // Log detected environment (dev only)
  if (import.meta.env.DEV) {
    console.log('Browser fixes initialized:', {
      isSafari: isSafari(),
      isIOS: isIOS(),
      isAndroid: isAndroid(),
      isMobile: isMobile()
    });
  }
};
