import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { formatAmount, formatDateIL, DEFAULT_CATEGORIES } from '@/types/receipt.types';
import type { Receipt } from '@/types/receipt.types';

/**
 * Generate PDF report from receipts
 */
export const generatePDFExport = async (
  receipts: Receipt[],
  businessName: string = 'עסק',
  includeImages: boolean = false
): Promise<Blob> => {
  // Create PDF document (A4, portrait)
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });
  
  // Load Hebrew font (Noto Sans Hebrew from Google Fonts)
  // Note: In production, you should embed the font properly
  doc.setLanguage('he');
  
  let currentY = 20;
  
  // Header
  currentY = addHeader(doc, businessName, currentY);
  
  // Summary section
  currentY = addSummary(doc, receipts, currentY);
  
  // Category breakdown
  currentY = addCategoryBreakdown(doc, receipts, currentY);
  
  // Add new page for details
  doc.addPage();
  currentY = 20;
  
  // Receipts table
  currentY = addReceiptsTable(doc, receipts, currentY);
  
  // If include images, add receipt images
  if (includeImages) {
    await addReceiptImages(doc, receipts);
  }
  
  // Footer on all pages
  addFooter(doc);
  
  // Generate blob
  return doc.output('blob');
};

/**
 * Add header to PDF
 */
const addHeader = (doc: jsPDF, businessName: string, y: number): number => {
  // Title
  doc.setFontSize(24);
  doc.setFont('helvetica', 'bold');
  doc.text('דוח הוצאות עסקיות', doc.internal.pageSize.width / 2, y, { align: 'center' });
  
  y += 10;
  
  // Business name
  doc.setFontSize(16);
  doc.setFont('helvetica', 'normal');
  doc.text(businessName, doc.internal.pageSize.width / 2, y, { align: 'center' });
  
  y += 8;
  
  // Date
  doc.setFontSize(10);
  doc.setTextColor(100);
  doc.text(
    `תאריך יצירה: ${new Date().toLocaleDateString('he-IL')}`,
    doc.internal.pageSize.width / 2,
    y,
    { align: 'center' }
  );
  
  y += 10;
  
  // Horizontal line
  doc.setDrawColor(200);
  doc.line(20, y, doc.internal.pageSize.width - 20, y);
  
  return y + 8;
};

/**
 * Add summary section
 */
const addSummary = (doc: jsPDF, receipts: Receipt[], y: number): number => {
  const totalAmount = receipts.reduce((sum, r) => sum + r.totalAmount, 0);
  const totalVat = receipts.reduce((sum, r) => sum + r.vatAmount, 0);
  const totalPreVat = receipts.reduce((sum, r) => sum + r.preVatAmount, 0);
  
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(0);
  doc.text('סיכום כספי', 20, y);
  
  y += 8;
  
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  
  const summaryData = [
    ['מספר קבלות:', receipts.length.toString()],
    ['סך הוצאות לפני מע"מ:', formatAmount(totalPreVat)],
    ['סך מע"מ (18%):', formatAmount(totalVat)],
    ['סך כל ההוצאות:', formatAmount(totalAmount)]
  ];
  
  summaryData.forEach(([label, value]) => {
    doc.setFont('helvetica', 'normal');
    doc.text(label, 20, y);
    doc.setFont('helvetica', 'bold');
    doc.text(value, 80, y);
    y += 6;
  });
  
  return y + 5;
};

/**
 * Add category breakdown
 */
const addCategoryBreakdown = (doc: jsPDF, receipts: Receipt[], y: number): number => {
  const totalAmount = receipts.reduce((sum, r) => sum + r.totalAmount, 0);
  
  // Group by category
  const categoryMap = new Map<string, { count: number; amount: number }>();
  
  receipts.forEach(receipt => {
    const existing = categoryMap.get(receipt.categoryId) || { count: 0, amount: 0 };
    categoryMap.set(receipt.categoryId, {
      count: existing.count + 1,
      amount: existing.amount + receipt.totalAmount
    });
  });
  
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('התפלגות לפי קטגוריות', 20, y);
  
  y += 8;
  
  const categoryData = Array.from(categoryMap.entries())
    .map(([categoryId, data]) => {
      const category = DEFAULT_CATEGORIES.find(c => c.id === categoryId);
      const percentage = totalAmount > 0 ? (data.amount / totalAmount) * 100 : 0;
      
      return [
        category?.nameHe || 'אחר',
        data.count.toString(),
        formatAmount(data.amount),
        `${percentage.toFixed(1)}%`
      ];
    })
    .sort((a, b) => parseFloat(b[3]) - parseFloat(a[3])); // Sort by percentage
  
  autoTable(doc, {
    startY: y,
    head: [['קטגוריה', 'קבלות', 'סכום', 'אחוז']],
    body: categoryData,
    theme: 'grid',
    styles: {
      font: 'helvetica',
      fontSize: 9,
      cellPadding: 3
    },
    headStyles: {
      fillColor: [37, 99, 235], // Primary blue
      textColor: 255,
      fontStyle: 'bold'
    },
    columnStyles: {
      0: { halign: 'right', cellWidth: 60 },
      1: { halign: 'center', cellWidth: 30 },
      2: { halign: 'right', cellWidth: 40 },
      3: { halign: 'center', cellWidth: 30 }
    }
  });
  
  return (doc as any).lastAutoTable.finalY + 10;
};

/**
 * Add receipts table
 */
const addReceiptsTable = (doc: jsPDF, receipts: Receipt[], y: number): number => {
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('פירוט קבלות', 20, y);
  
  y += 8;
  
  const tableData = receipts
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .map(receipt => {
      const category = DEFAULT_CATEGORIES.find(c => c.id === receipt.categoryId);
      
      return [
        formatDateIL(receipt.date),
        receipt.vendorName,
        category?.nameHe || 'אחר',
        formatAmount(receipt.preVatAmount),
        formatAmount(receipt.vatAmount),
        formatAmount(receipt.totalAmount)
      ];
    });
  
  autoTable(doc, {
    startY: y,
    head: [['תאריך', 'עסק', 'קטגוריה', 'לפני מע"מ', 'מע"מ', 'כולל']],
    body: tableData,
    theme: 'striped',
    styles: {
      font: 'helvetica',
      fontSize: 8,
      cellPadding: 2
    },
    headStyles: {
      fillColor: [37, 99, 235],
      textColor: 255,
      fontStyle: 'bold'
    },
    columnStyles: {
      0: { halign: 'center', cellWidth: 25 },
      1: { halign: 'right', cellWidth: 45 },
      2: { halign: 'right', cellWidth: 35 },
      3: { halign: 'right', cellWidth: 25 },
      4: { halign: 'right', cellWidth: 20 },
      5: { halign: 'right', cellWidth: 25 }
    },
    didDrawPage: () => {
      // Add page numbers
      const pageCount = doc.getNumberOfPages();
      const currentPage = (doc as any).internal.getCurrentPageInfo().pageNumber;
      
      doc.setFontSize(8);
      doc.setTextColor(150);
      doc.text(
        `עמוד ${currentPage} מתוך ${pageCount}`,
        doc.internal.pageSize.width / 2,
        doc.internal.pageSize.height - 10,
        { align: 'center' }
      );
    }
  });
  
  return (doc as any).lastAutoTable.finalY + 10;
};

/**
 * Add receipt images (if includeImages is true)
 */
const addReceiptImages = async (doc: jsPDF, receipts: Receipt[]): Promise<void> => {
  for (let i = 0; i < receipts.length; i++) {
    const receipt = receipts[i];
    
    if (!receipt.imageUrl) continue;
    
    // Add new page for each image
    doc.addPage();
    
    try {
      // Load image
      const img = await loadImage(receipt.imageUrl);
      
      // Calculate dimensions to fit page
      const pageWidth = doc.internal.pageSize.width - 40; // 20mm margin each side
      const pageHeight = doc.internal.pageSize.height - 60; // Top and bottom margins
      
      const imgRatio = img.width / img.height;
      let imgWidth = pageWidth;
      let imgHeight = imgWidth / imgRatio;
      
      if (imgHeight > pageHeight) {
        imgHeight = pageHeight;
        imgWidth = imgHeight * imgRatio;
      }
      
      const x = (doc.internal.pageSize.width - imgWidth) / 2;
      const y = 40;
      
      // Add image title
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.text(`קבלה: ${receipt.vendorName}`, doc.internal.pageSize.width / 2, 25, { align: 'center' });
      
      // Add image
      doc.addImage(img.src, 'JPEG', x, y, imgWidth, imgHeight);
      
      // Add caption
      doc.setFontSize(9);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(100);
      doc.text(
        `${formatDateIL(receipt.date)} | ${formatAmount(receipt.totalAmount)}`,
        doc.internal.pageSize.width / 2,
        y + imgHeight + 10,
        { align: 'center' }
      );
      
    } catch (error) {
      console.error('Failed to load image:', error);
      // Continue with next image
    }
  }
};

/**
 * Load image as promise
 */
const loadImage = (url: string): Promise<HTMLImageElement> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = url;
  });
};

/**
 * Add footer to all pages
 */
const addFooter = (doc: jsPDF): void => {
  const pageCount = doc.getNumberOfPages();
  
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    
    // Footer line
    doc.setDrawColor(200);
    doc.line(20, doc.internal.pageSize.height - 20, doc.internal.pageSize.width - 20, doc.internal.pageSize.height - 20);
    
    // Footer text
    doc.setFontSize(8);
    doc.setTextColor(100);
    doc.text(
      'נוצר באמצעות Tik-Tax | מערכת ניהול קבלות',
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 12,
      { align: 'center' }
    );
  }
};
