# Test file for the Invoice Generator
# Run this to test the core functionality

from invoice_generator import InvoiceGenerator
import os

def test_basic_invoice():
    """Test basic invoice generation"""
    print("Testing basic invoice generation...")
    
    # Create invoice
    invoice = InvoiceGenerator()
    
    # Set business info
    invoice.set_business_info(
        name="TechCorp Solutions",
        address="123 Tech Street, Silicon Valley, CA 94000",
        phone="(555) 123-4567",
        email="info@techcorp.com"
    )
    
    # Set client info
    invoice.set_client_info(
        name="ABC Company",
        address="456 Business Ave, New York, NY 10001",
        phone="(555) 987-6543",
        email="contact@abccompany.com"
    )
    
    # Set invoice details
    invoice.set_invoice_details(
        invoice_number="TEST-001",
        tax_rate=8.5,
        discount=5.0,
        payment_terms="Net 30 days"
    )
    
    # Add items
    invoice.add_item("Website Development", 1, 2500.00)
    invoice.add_item("Logo Design", 1, 500.00)
    invoice.add_item("SEO Optimization", 3, 200.00)
    invoice.add_item("Domain Registration", 1, 15.00)
    invoice.add_item("Web Hosting (1 year)", 1, 120.00)
    
    # Generate invoice
    try:
        pdf_file = invoice.generate_pdf()
        json_file = invoice.save_invoice_data()
        
        print(f"✅ PDF generated: {pdf_file}")
        print(f"✅ JSON saved: {json_file}")
        
        # Display totals
        totals = invoice.calculate_totals()
        print(f"\n💰 Invoice Totals:")
        print(f"   Subtotal: ${totals['subtotal']:.2f}")
        print(f"   Discount: -${totals['discount_amount']:.2f}")
        print(f"   Tax: ${totals['tax_amount']:.2f}")
        print(f"   TOTAL: ${totals['total']:.2f}")
        
        # Verify files exist
        if os.path.exists(pdf_file) and os.path.exists(json_file):
            print("\n✅ Test PASSED: Files created successfully!")
            return True
        else:
            print("\n❌ Test FAILED: Files not created!")
            return False
            
    except Exception as e:
        print(f"\n❌ Test FAILED: {str(e)}")
        return False

def test_calculations():
    """Test calculation accuracy"""
    print("\nTesting calculations...")
    
    invoice = InvoiceGenerator()
    
    # Add test items
    invoice.add_item("Item 1", 2, 100.00)  # $200
    invoice.add_item("Item 2", 1, 50.00)   # $50
    # Total: $250
    
    # Set 10% tax and 5% discount
    invoice.set_invoice_details("CALC-TEST", tax_rate=10.0, discount=5.0)
    
    totals = invoice.calculate_totals()
    
    expected_subtotal = 250.00
    expected_discount = 12.50  # 5% of 250
    expected_taxable = 237.50  # 250 - 12.50
    expected_tax = 23.75       # 10% of 237.50
    expected_total = 261.25    # 237.50 + 23.75
    
    print(f"Subtotal: ${totals['subtotal']:.2f} (expected: ${expected_subtotal:.2f})")
    print(f"Discount: ${totals['discount_amount']:.2f} (expected: ${expected_discount:.2f})")
    print(f"Tax: ${totals['tax_amount']:.2f} (expected: ${expected_tax:.2f})")
    print(f"Total: ${totals['total']:.2f} (expected: ${expected_total:.2f})")
    
    # Check if calculations are correct (within 0.01 tolerance)
    tolerance = 0.01
    if (abs(totals['subtotal'] - expected_subtotal) < tolerance and
        abs(totals['discount_amount'] - expected_discount) < tolerance and
        abs(totals['tax_amount'] - expected_tax) < tolerance and
        abs(totals['total'] - expected_total) < tolerance):
        print("✅ Calculations test PASSED!")
        return True
    else:
        print("❌ Calculations test FAILED!")
        return False

def test_export_functionality():
    """Test export functionality"""
    print("\nTesting export functionality...")
    
    try:
        from invoice_exporter import InvoiceExporter
        
        exporter = InvoiceExporter()
        
        # Check if test invoice exists
        test_invoice = exporter.load_invoice_from_json("TEST-001")
        
        if test_invoice:
            # Test CSV export
            csv_file = exporter.export_to_csv(test_invoice, "test_export.csv")
            
            if os.path.exists(csv_file):
                print(f"✅ CSV export test PASSED: {csv_file}")
                return True
            else:
                print("❌ CSV export test FAILED: File not created")
                return False
        else:
            print("❌ Export test FAILED: Test invoice not found (run basic test first)")
            return False
            
    except Exception as e:
        print(f"❌ Export test FAILED: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Invoice Generator Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Invoice Generation", test_basic_invoice),
        ("Calculation Accuracy", test_calculations),
        ("Export Functionality", test_export_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED!")
    else:
        print("⚠️  Some tests FAILED!")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()
