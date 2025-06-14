#!/usr/bin/env python3
"""
Gmail Connection Test Script - আপনার Gmail settings check করার জন্য
"""

from email_sender import EmailSender
import sys

def test_gmail_connection():
    """Test Gmail connection with your credentials"""
    
    print("📧 Gmail Connection Test")
    print("=" * 40)
      # Your Gmail credentials
    email = "marketerrobi@gmail.com"
    password = "moogtnzzgqgzfbpr"
    
    print(f"Testing email: {email}")
    print("Testing password: [HIDDEN]")
    print()
    
    # Test connection
    email_sender = EmailSender()
    
    print("🔄 Testing Gmail connection...")
    success, message = email_sender.test_email_connection(email, password)
    
    if success:
        print("✅ SUCCESS! Gmail connection working perfectly!")
        print()
        print("🎯 Your email setup is correct. You can send invoices now!")
        return True
    else:
        print("❌ FAILED! Gmail connection not working.")
        print(f"Error: {message}")
        print()
        print("🔧 TROUBLESHOOTING STEPS:")
        print("1. 📱 Enable 2-Factor Authentication:")
        print("   - Go to myaccount.google.com")
        print("   - Security > 2-Step Verification > Turn On")
        print()
        print("2. 🔑 Generate App Password:")
        print("   - Go to myaccount.google.com")
        print("   - Security > App passwords")
        print("   - Select app: Mail")
        print("   - Generate password")
        print("   - Use that 16-character password instead")
        print()
        print("3. ✅ Common fixes:")
        print("   - Don't use your regular Gmail password")
        print("   - Use App Password (looks like: abcd efgh ijkl mnop)")
        print("   - Make sure 2FA is enabled first")
        print("   - Check internet connection")
        print()
        print("4. 🌐 Alternative test:")
        print("   - Try sending a regular email from Gmail")
        print("   - Make sure your account is not locked")
        
        return False

def test_send_real_email():
    """Test sending actual email"""
    
    # Only run if connection test passes
    if not test_gmail_connection():
        return False
    
    print("\n" + "=" * 40)
    print("📤 REAL EMAIL TEST")
    print("=" * 40)
    
    recipient = input("Enter recipient email for test (or press Enter to skip): ").strip()
    
    if not recipient:
        print("⏭️ Skipping real email test")
        return True
    
    print(f"🎯 Sending test email to: {recipient}")
    
    # Create a test invoice file path (use existing invoice)
    import os
    
    # Find any existing invoice
    invoice_files = [f for f in os.listdir('invoices') if f.endswith('.pdf')]
    
    if not invoice_files:
        print("❌ No invoice PDFs found. Create an invoice first.")
        return False
    
    test_pdf = f"invoices/{invoice_files[0]}"
    invoice_number = invoice_files[0].replace('invoice_', '').replace('.pdf', '')    
    print(f"📄 Using test invoice: {invoice_number}")
    
    email_sender = EmailSender()
    
    success, message = email_sender.send_invoice_email(
        sender_email="marketerrobi@gmail.com",
        sender_password="moogtnzzgqgzfbpr",
        recipient_email=recipient,
        invoice_pdf_path=test_pdf,
        invoice_number=invoice_number,
        client_name="Test Client",
        business_name="Marketer Robi",
        email_subject=f"Test Invoice from Marketer Robi - #{invoice_number}",
        email_message=f"""Dear Test Client,

This is a test email from your invoice generator system.

Invoice #{invoice_number} is attached for testing purposes.

Best regards,
Marketer Robi
marketerrobi@gmail.com"""
    )
    
    if success:
        print(f"✅ Test email sent successfully!")
        print(f"📧 Check {recipient} for the test invoice")
        return True
    else:
        print(f"❌ Test email failed: {message}")
        return False

if __name__ == "__main__":
    print("🚀 Gmail Setup Diagnostic Tool")
    print("==============================")
    
    # Test connection
    connection_ok = test_gmail_connection()
    
    if connection_ok:
        print("\n🎉 CONNECTION TEST PASSED!")
        
        # Ask if user wants to test real email
        test_real = input("\nDo you want to test sending a real email? (y/n): ").strip().lower()
        
        if test_real in ['y', 'yes']:
            email_ok = test_send_real_email()
            if email_ok:
                print("\n🎉 ALL TESTS PASSED! Your email system is working perfectly!")
            else:
                print("\n❌ Email sending test failed. Check the error above.")
        else:
            print("\n✅ Connection test passed. Your email setup should work!")
    else:
        print("\n❌ CONNECTION TEST FAILED!")
        print("Please follow the troubleshooting steps above.")
        
    print("\n" + "=" * 50)
    print("📞 Need help? Check the troubleshooting guide above.")
