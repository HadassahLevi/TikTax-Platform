import React, { useState, useEffect } from 'react';
import { Keyboard } from 'lucide-react';
import Modal from '@/components/ui/Modal';
import { KEYBOARD_SHORTCUTS } from '@/hooks/useKeyboardShortcuts';

export const KeyboardShortcutsModal: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
  const modifierKey = isMac ? '⌘' : 'Ctrl';

  // Listen for custom event to open modal
  useEffect(() => {
    const handleShowShortcuts = () => setIsOpen(true);
    document.addEventListener('showKeyboardShortcuts', handleShowShortcuts);
    return () => document.removeEventListener('showKeyboardShortcuts', handleShowShortcuts);
  }, []);

  const formatShortcut = (shortcut: typeof KEYBOARD_SHORTCUTS[0]) => {
    const keys: string[] = [];
    
    if (shortcut.ctrlOrCmd) keys.push(modifierKey);
    if (shortcut.shift) keys.push('Shift');
    if (shortcut.alt) keys.push('Alt');
    keys.push(shortcut.key);
    
    return keys;
  };

  return (
    <>
      {/* Trigger Button - Add to Header */}
      <button
        onClick={() => setIsOpen(true)}
        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        title="קיצורי מקלדת (Shift + ?)"
        aria-label="הצג קיצורי מקלדת"
      >
        <Keyboard className="w-5 h-5 text-gray-700" />
      </button>

      {/* Shortcuts Modal */}
      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="קיצורי מקלדת"
        size="md"
      >
        <div className="space-y-1">
          {KEYBOARD_SHORTCUTS.map((shortcut, index) => (
            <div
              key={index}
              className="flex items-center justify-between py-3 px-2 hover:bg-gray-50 rounded-lg transition-colors"
            >
              <span className="text-gray-700 text-sm">{shortcut.description}</span>
              
              <div className="flex items-center gap-1">
                {formatShortcut(shortcut).map((key, i, arr) => (
                  <React.Fragment key={i}>
                    <kbd className="
                      px-2.5 py-1.5 
                      bg-white 
                      border border-gray-300 
                      rounded 
                      text-xs 
                      font-mono 
                      font-semibold 
                      text-gray-700
                      shadow-sm
                      min-w-[32px]
                      text-center
                    ">
                      {key}
                    </kbd>
                    {i < arr.length - 1 && (
                      <span className="text-gray-400 text-xs mx-0.5">+</span>
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Pro Tips Section */}
        <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-primary-50 rounded-lg border border-blue-100">
          <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <span>💡</span>
            <span>טיפים מקצועיים</span>
          </h4>
          <ul className="text-sm text-gray-700 space-y-1.5">
            <li>• לחץ על <kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs">?</kbd> בכל עמוד לראות את הרשימה הזו</li>
            <li>• השתמש ב-<kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs">Tab</kbd> לניווט בין שדות בטפסים</li>
            <li>• <kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs">ESC</kbd> סוגר תמיד את החלון הפתוח האחרון</li>
            <li>• השתמש בחצים <kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs">↑↓</kbd> לניווט ברשימות</li>
          </ul>
        </div>

        {/* Platform Info */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            אתה משתמש ב-{isMac ? 'Mac' : 'Windows/Linux'} • 
            {isMac ? ' השתמש ב-⌘ (Command)' : ' השתמש ב-Ctrl'}
          </p>
        </div>
      </Modal>
    </>
  );
};
