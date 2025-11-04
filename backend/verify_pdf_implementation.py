"""
PDF Export - Quick Verification Script
Checks that all components are properly installed and working
"""

import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("=" * 60)
    print("CHECKING DEPENDENCIES")
    print("=" * 60)
    
    dependencies = {
        'reportlab': 'ReportLab PDF generation',
        'PyPDF2': 'PDF manipulation (optional)',
        'PIL': 'Image processing (Pillow)'
    }
    
    missing = []
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module:20s} - {description}")
        except ImportError:
            print(f"❌ {module:20s} - {description} (MISSING)")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ All dependencies installed")
        return True


def check_service_file():
    """Check if PDF service file exists"""
    print("\n" + "=" * 60)
    print("CHECKING SERVICE FILE")
    print("=" * 60)
    
    service_file = Path(__file__).parent / "app" / "services" / "pdf_service.py"
    
    if service_file.exists():
        print(f"✅ PDF service file exists: {service_file}")
        
        # Check file size
        size = service_file.stat().st_size
        print(f"✅ File size: {size:,} bytes")
        
        if size > 1000:
            print(f"✅ File has content (>1 KB)")
            return True
        else:
            print(f"❌ File is too small (<1 KB)")
            return False
    else:
        print(f"❌ PDF service file not found: {service_file}")
        return False


def check_import():
    """Check if PDF service can be imported"""
    print("\n" + "=" * 60)
    print("CHECKING IMPORT")
    print("=" * 60)
    
    try:
        # Add backend to path
        backend_path = Path(__file__).parent
        sys.path.insert(0, str(backend_path))
        
        from app.services.pdf_service import pdf_service, PDFService
        
        print(f"✅ Successfully imported PDFService")
        print(f"✅ pdf_service singleton exists: {pdf_service}")
        print(f"✅ Type: {type(pdf_service)}")
        
        # Check methods
        methods = ['generate_export', '_create_title_page', '_create_summary_section']
        for method in methods:
            if hasattr(pdf_service, method):
                print(f"✅ Method exists: {method}")
            else:
                print(f"❌ Method missing: {method}")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def check_endpoint():
    """Check if export endpoint is updated"""
    print("\n" + "=" * 60)
    print("CHECKING ENDPOINT")
    print("=" * 60)
    
    endpoint_file = Path(__file__).parent / "app" / "api" / "v1" / "endpoints" / "export.py"
    
    if not endpoint_file.exists():
        print(f"❌ Endpoint file not found: {endpoint_file}")
        return False
    
    print(f"✅ Endpoint file exists: {endpoint_file}")
    
    # Check if pdf_service is imported
    content = endpoint_file.read_text()
    
    checks = [
        ('from app.services.pdf_service import pdf_service', 'PDF service import'),
        ('elif request.format == ExportFormat.PDF:', 'PDF format handling'),
        ('pdf_service.generate_export', 'PDF service call'),
        ('mime_type = "application/pdf"', 'PDF mime type')
    ]
    
    all_found = True
    for pattern, description in checks:
        if pattern in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description} (not found)")
            all_found = False
    
    return all_found


def check_tests():
    """Check if test files exist"""
    print("\n" + "=" * 60)
    print("CHECKING TESTS")
    print("=" * 60)
    
    test_files = [
        ("tests/services/test_pdf_service.py", "Unit tests"),
        ("tests/integration/test_pdf_export.py", "Integration tests"),
        ("test_pdf_manual.py", "Manual test script")
    ]
    
    backend_path = Path(__file__).parent
    all_exist = True
    
    for file_path, description in test_files:
        full_path = backend_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {description:30s} ({size:,} bytes)")
        else:
            print(f"❌ {description:30s} (not found)")
            all_exist = False
    
    return all_exist


def check_documentation():
    """Check if documentation exists"""
    print("\n" + "=" * 60)
    print("CHECKING DOCUMENTATION")
    print("=" * 60)
    
    doc_files = [
        ("PDF_EXPORT_DOCUMENTATION.md", "Complete documentation"),
        ("PDF_EXPORT_QUICK_REFERENCE.md", "Quick reference"),
        ("PDF_IMPLEMENTATION_SUMMARY.md", "Implementation summary")
    ]
    
    backend_path = Path(__file__).parent
    all_exist = True
    
    for file_path, description in doc_files:
        full_path = backend_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            lines = len(full_path.read_text().splitlines())
            print(f"✅ {description:30s} ({lines} lines, {size:,} bytes)")
        else:
            print(f"❌ {description:30s} (not found)")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("PDF EXPORT - VERIFICATION")
    print("=" * 60)
    print()
    
    results = {
        "Dependencies": check_dependencies(),
        "Service File": check_service_file(),
        "Import": check_import(),
        "Endpoint": check_endpoint(),
        "Tests": check_tests(),
        "Documentation": check_documentation()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10s} {check_name}")
    
    total_passed = sum(results.values())
    total_checks = len(results)
    
    print(f"\nTotal: {total_passed}/{total_checks} checks passed")
    
    if total_passed == total_checks:
        print("\n🎉 ALL CHECKS PASSED - PDF Export is ready!")
        print("\nNext steps:")
        print("1. Run unit tests: pytest tests/services/test_pdf_service.py -v")
        print("2. Run integration tests: pytest tests/integration/test_pdf_export.py -v")
        print("3. Run manual test: python test_pdf_manual.py")
        print("4. Deploy to staging environment")
        return 0
    else:
        print(f"\n⚠️  {total_checks - total_passed} check(s) failed")
        print("\nPlease fix the issues above before deploying.")
        return 1


if __name__ == "__main__":
    exit(main())
