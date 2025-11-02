import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-primary-600 mb-4">
            ברוכים הבאים ל-Tik-Tax
          </h1>
          <p className="text-xl text-gray-700 mb-6">
            מערכת ניהול קבלות חכמה לעסקים קטנים
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            <div className="p-6 bg-primary-50 rounded-lg">
              <div className="text-3xl mb-2">📸</div>
              <h3 className="font-semibold text-primary-900 mb-2">צלם קבלה</h3>
              <p className="text-sm text-gray-600">
                צלם את הקבלה והמערכת תחלץ את הפרטים אוטומטית
              </p>
            </div>
            
            <div className="p-6 bg-success-50 rounded-lg">
              <div className="text-3xl mb-2">✓</div>
              <h3 className="font-semibold text-success-900 mb-2">אשר ושמור</h3>
              <p className="text-sm text-gray-600">
                בדוק את הפרטים ושמור בארכיון המאובטח
              </p>
            </div>
            
            <div className="p-6 bg-info-50 rounded-lg">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold text-info-900 mb-2">ייצא לאקסל</h3>
              <p className="text-sm text-gray-600">
                ייצא את כל הקבלות לקובץ Excel עבור הרו"ח
              </p>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <button className="w-full md:w-auto px-8 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors">
              התחל עכשיו
            </button>
            <p className="text-sm text-gray-500">
              הפרויקט מוכן לפיתוח • React 18.2 + TypeScript + Tailwind CSS
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
