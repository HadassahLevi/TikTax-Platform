"""
Quick Test Runner for Receipt CRUD Endpoints
Run this to verify implementation
"""

import sys
import subprocess

def run_tests():
    """Run all receipt CRUD tests"""
    print("=" * 70)
    print("RUNNING RECEIPT CRUD TESTS")
    print("=" * 70)
    
    # Test commands
    tests = [
        {
            "name": "Unit Tests - Receipt CRUD",
            "command": ["pytest", "tests/api/test_receipt_crud.py", "-v", "--tb=short"]
        },
        {
            "name": "Integration Tests - Receipt CRUD",
            "command": ["pytest", "tests/integration/test_receipt_crud_integration.py", "-v", "--tb=short"]
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n\n{'=' * 70}")
        print(f"TEST: {test['name']}")
        print("=" * 70)
        
        try:
            result = subprocess.run(
                test["command"],
                cwd="c:/TikTax/backend",
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            success = result.returncode == 0
            results.append({
                "name": test["name"],
                "success": success,
                "returncode": result.returncode
            })
            
        except Exception as e:
            print(f"ERROR running test: {e}")
            results.append({
                "name": test["name"],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} - {result['name']}")
        if not result["success"] and "error" in result:
            print(f"   Error: {result['error']}")
    
    # Overall result
    all_passed = all(r["success"] for r in results)
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(run_tests())
