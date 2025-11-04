"""
Manual Integration Test for Receipt Upload
Run this script to test the complete upload flow
"""

import requests
import os
from pathlib import Path
from PIL import Image
import io

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_USER_EMAIL = "test@tiktax.co.il"
TEST_USER_PASSWORD = "Test123456!"


def create_test_image():
    """Create a test receipt image"""
    img = Image.new('RGB', (800, 600), color='white')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes


def test_upload_flow():
    """Test complete upload and status flow"""
    print("���� Testing Receipt Upload Flow\n")
    
    # Step 1: Login
    print("1������  Logging in...")
    login_response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
    )
    
    if login_response.status_code != 200:
        print(f"��� Login failed: {login_response.status_code}")
        print(f"   {login_response.json()}")
        return
    
    tokens = login_response.json()
    access_token = tokens['access_token']
    print(f"��� Logged in successfully")
    print(f"   Token: {access_token[:20]}...\n")
    
    # Step 2: Create test image
    print("2������  Creating test receipt image...")
    test_image = create_test_image()
    print("��� Test image created (800x600 JPEG)\n")
    
    # Step 3: Upload receipt
    print("3������  Uploading receipt...")
    files = {
        'file': ('test_receipt.jpg', test_image, 'image/jpeg')
    }
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    upload_response = requests.post(
        f"{API_BASE_URL}/receipts/upload",
        files=files,
        headers=headers
    )
    
    if upload_response.status_code != 201:
        print(f"��� Upload failed: {upload_response.status_code}")
        print(f"   {upload_response.json()}")
        return
    
    upload_data = upload_response.json()
    receipt_id = upload_data['receipt_id']
    print(f"��� Receipt uploaded successfully")
    print(f"   Receipt ID: {receipt_id}")
    print(f"   Status: {upload_data['status']}")
    print(f"   Message: {upload_data['message']}\n")
    
    # Step 4: Poll processing status
    print("4������  Checking processing status...")
    import time
    
    for i in range(10):
        status_response = requests.get(
            f"{API_BASE_URL}/receipts/{receipt_id}/status",
            headers=headers
        )
        
        if status_response.status_code != 200:
            print(f"��� Status check failed: {status_response.status_code}")
            return
        
        status_data = status_response.json()
        status = status_data['status']
        progress = status_data['progress']
        message = status_data['message']
        
        print(f"   [{i+1}/10] Status: {status} | Progress: {progress}% | {message}")
        
        if status in ['review', 'approved', 'failed']:
            print(f"\n��� Processing complete!")
            
            if status == 'review' and status_data.get('ocr_data'):
                print("\n���� OCR Results:")
                ocr_data = status_data['ocr_data']
                print(f"   Vendor: {ocr_data.get('vendor_name')}")
                print(f"   Business #: {ocr_data.get('business_number')}")
                print(f"   Amount: ���{ocr_data.get('total_amount')}")
                print(f"   VAT: ���{ocr_data.get('vat_amount')}")
            
            break
        
        time.sleep(2)
    else:
        print("\n������  Processing timeout (still processing after 20 seconds)")
    
    print("\n" + "="*60)
    print("���� Test completed!")
    print("="*60)


def test_file_validation():
    """Test file validation errors"""
    print("\n���� Testing File Validation\n")
    
    # Login first
    login_response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
    )
    
    if login_response.status_code != 200:
        print("��� Login failed")
        return
    
    access_token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test 1: Invalid file type
    print("1������  Testing invalid file type (text)...")
    files = {
        'file': ('document.txt', io.BytesIO(b'Not an image'), 'text/plain')
    }
    response = requests.post(
        f"{API_BASE_URL}/receipts/upload",
        files=files,
        headers=headers
    )
    
    if response.status_code == 400 and '������ ��������' in response.json()['detail']:
        print("��� Correctly rejected invalid file type\n")
    else:
        print(f"��� Unexpected response: {response.status_code}\n")
    
    # Test 2: File too small
    print("2������  Testing file too small (5KB)...")
    small_data = b'x' * (5 * 1024)
    files = {
        'file': ('small.jpg', io.BytesIO(small_data), 'image/jpeg')
    }
    response = requests.post(
        f"{API_BASE_URL}/receipts/upload",
        files=files,
        headers=headers
    )
    
    if response.status_code == 400 and '������ ������' in response.json()['detail']:
        print("��� Correctly rejected small file\n")
    else:
        print(f"��� Unexpected response: {response.status_code}\n")
    
    # Test 3: File too large (would take too long to upload, skip)
    print("3������  Skipping large file test (would take too long)\n")
    
    print("="*60)
    print("���� Validation tests completed!")
    print("="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  TIK-TAX RECEIPT UPLOAD INTEGRATION TEST")
    print("="*60)
    print("\nPrerequisites:")
    print(f"  - Backend running on {API_BASE_URL}")
    print(f"  - Test user: {TEST_USER_EMAIL}")
    print(f"  - AWS S3 credentials configured")
    print("\n" + "="*60 + "\n")
    
    try:
        # Run main upload flow test
        test_upload_flow()
        
        # Run validation tests
        test_file_validation()
        
    except requests.exceptions.ConnectionError:
        print("\n��� ERROR: Could nxxxxxxxxct to backend")
        print("   Make sure the server is running on http://localhost:8000")
    except KeyboardInterrupt:
        print("\n\n������  Test interrupted by user")
    except Exception as e:
        print(f"\n��� ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
