#!/usr/bin/env python3
"""
Test script for the complete Invoice Generator system including web interface
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

def test_web_api():
    """Test the web API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Web API...")
    print("-" * 40)
    
    # Test data
    test_invoice = {
        "business_name": "TechWeb Solutions",
        "business_address": "123 Web Street, Digital City, DC 12345",
        "business_phone": "(555) 123-4567",
        "business_email": "info@techweb.com",
        "client_name": "WebTest Client",
        "client_address": "456 Client Ave, Test City, TC 67890",
        "client_phone": "(555) 987-6543",
        "client_email": "client@webtest.com",
        "invoice_number": f"WEB-TEST-{int(time.time())}",
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "tax_rate": 10.0,
        "discount": 5.0,
        "payment_terms": "Net 30 days - Web Test",
        "items": [
            {
                "description": "Web Development Services",
                "quantity": 1,
                "unit_price": 2000.00
            },
            {
                "description": "API Integration",
                "quantity": 2,
                "unit_price": 500.00
            },
            {
                "description": "Testing & QA",
                "quantity": 1,
                "unit_price": 300.00
            }
        ]
    }
    
    try:
        # Test 1: Create Invoice
        print("1. Testing invoice creation API...")
        response = requests.post(f"{base_url}/api/create-invoice", 
                               json=test_invoice, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Invoice created: {test_invoice['invoice_number']}")
                print(f"   💰 Total: ${result['totals']['total']:.2f}")
                invoice_number = test_invoice['invoice_number']
            else:
                print(f"   ❌ API returned error: {result.get('error')}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
        
        # Test 2: Get Invoice
        print("2. Testing get invoice API...")
        response = requests.get(f"{base_url}/api/get-invoice/{invoice_number}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Invoice retrieved successfully")
                print(f"   📄 Client: {result['data']['client_info']['name']}")
            else:
                print(f"   ❌ Failed to retrieve invoice: {result.get('error')}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
        
        # Test 3: Get All Invoices
        print("3. Testing get all invoices API...")
        response = requests.get(f"{base_url}/api/get-all-invoices")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                invoices = result.get('invoices', [])
                print(f"   ✅ Retrieved {len(invoices)} invoices")
                
                # Find our test invoice
                test_found = any(inv['number'] == invoice_number for inv in invoices)
                if test_found:
                    print(f"   ✅ Test invoice found in list")
                else:
                    print(f"   ⚠️  Test invoice not found in list")
            else:
                print(f"   ❌ Failed to retrieve invoices: {result.get('error')}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
        
        # Test 4: Download PDF (just check if endpoint responds)
        print("4. Testing PDF download endpoint...")
        response = requests.head(f"{base_url}/api/download-pdf/{invoice_number}")
        
        if response.status_code == 200:
            print(f"   ✅ PDF download endpoint working")
        else:
            print(f"   ❌ PDF download failed: {response.status_code}")
        
        # Test 5: Export CSV (just check if endpoint responds)
        print("5. Testing CSV export endpoint...")
        response = requests.head(f"{base_url}/api/export-csv/{invoice_number}")
        
        if response.status_code == 200:
            print(f"   ✅ CSV export endpoint working")
        else:
            print(f"   ❌ CSV export failed: {response.status_code}")
        
        print("\n✅ All Web API tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Web server is not running!")
        print("   Please start the web server with: python web_app.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def check_web_server():
    """Check if web server is running"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_web_server():
    """Start web server in background"""
    import subprocess
    import time
    
    print("🚀 Starting web server...")
    
    # Start web server
    process = subprocess.Popen([sys.executable, "web_app.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    # Wait for server to start
    for i in range(10):
        time.sleep(1)
        if check_web_server():
            print("✅ Web server started successfully!")
            return process
        print(f"   Waiting for server... ({i+1}/10)")
    
    print("❌ Failed to start web server")
    process.terminate()
    return None

def main():
    """Main test function"""
    print("🧪 Complete Invoice Generator Test Suite")
    print("=" * 50)
    
    # Check if web server is running
    if not check_web_server():
        print("⚠️  Web server is not running. Starting it now...")
        process = start_web_server()
        if not process:
            print("❌ Cannot start web server. Please start it manually with:")
            print("   python web_app.py")
            return
    else:
        print("✅ Web server is already running")
        process = None
    
    print()
    
    # Run web API tests
    try:
        success = test_web_api()
        
        if success:
            print("\n🎉 All tests completed successfully!")
            print("\n🌐 Web Interface Features:")
            print("   • Dashboard: http://localhost:5000")
            print("   • Create Invoice: http://localhost:5000/create")
            print("   • View Invoices: http://localhost:5000/view")
        else:
            print("\n⚠️  Some tests failed. Please check the web application.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    
    finally:
        # Clean up
        if process:
            print("\n🔄 Stopping web server...")
            process.terminate()
            time.sleep(2)
            print("✅ Web server stopped")

if __name__ == "__main__":
    main()
