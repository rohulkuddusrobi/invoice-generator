#!/usr/bin/env python3
"""
Professional Invoice Generator - Main Application
This is the main entry point for the invoice generator application.
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from invoice_generator import InvoiceGenerator
from invoice_exporter import InvoiceExporter
from email_sender import EmailSender

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("           PROFESSIONAL INVOICE GENERATOR")
    print("=" * 60)
    print()

def print_menu():
    """Print main menu"""
    print("\nChoose an option:")
    print("1. Create New Invoice (Command Line)")
    print("2. Launch GUI Interface")
    print("3. Launch Web Interface")
    print("4. Export Invoice to CSV")
    print("5. Export All Invoices Summary")
    print("6. Send Invoice via Email")
    print("7. View Existing Invoices")
    print("8. Exit")
    print("-" * 30)

def create_cli_invoice():
    """Create invoice using command line interface"""
    print("\n📋 Creating New Invoice (CLI Mode)")
    print("-" * 40)
    
    # Create invoice generator instance
    invoice = InvoiceGenerator()
    
    try:
        # Get business information
        print("\n🏢 Business Information:")
        business_name = input("Business Name: ").strip()
        if not business_name:
            print("❌ Business name is required!")
            return
        
        business_address = input("Business Address: ").strip()
        business_phone = input("Business Phone: ").strip()
        business_email = input("Business Email (optional): ").strip()
        
        invoice.set_business_info(business_name, business_address, business_phone, business_email)
        
        # Get client information
        print("\n👤 Client Information:")
        client_name = input("Client Name: ").strip()
        if not client_name:
            print("❌ Client name is required!")
            return
        
        client_address = input("Client Address: ").strip()
        client_phone = input("Client Phone (optional): ").strip()
        client_email = input("Client Email (optional): ").strip()
        
        invoice.set_client_info(client_name, client_address, client_phone, client_email)
        
        # Get invoice details
        print("\n📄 Invoice Details:")
        invoice_number = input("Invoice Number: ").strip()
        if not invoice_number:
            print("❌ Invoice number is required!")
            return
        
        invoice_date = input("Invoice Date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not invoice_date:
            invoice_date = datetime.now().strftime("%Y-%m-%d")
        
        tax_rate = input("Tax Rate (%) or press Enter for 0: ").strip()
        tax_rate = float(tax_rate) if tax_rate else 0.0
        
        discount = input("Discount (%) or press Enter for 0: ").strip()
        discount = float(discount) if discount else 0.0
        
        payment_terms = input("Payment Terms (optional): ").strip()
        
        invoice.set_invoice_details(invoice_number, invoice_date, tax_rate, discount, payment_terms)
        
        # Get items
        print("\n📦 Items/Services:")
        print("Enter items one by one. Type 'done' when finished.")
        
        while True:
            print("\n" + "-" * 20)
            description = input("Item Description (or 'done' to finish): ").strip()
            if description.lower() == 'done':
                break
            
            if not description:
                print("❌ Description cannot be empty!")
                continue
            
            try:
                quantity = float(input("Quantity: "))
                unit_price = float(input("Unit Price: $"))
                
                invoice.add_item(description, quantity, unit_price)
                print(f"✅ Added: {description} - Qty: {quantity} - Price: ${unit_price:.2f}")
                
            except ValueError:
                print("❌ Please enter valid numbers for quantity and price!")
                continue
        
        if not invoice.items:
            print("❌ At least one item is required!")
            return
        
        # Generate invoice
        print("\n🔄 Generating invoice...")
        pdf_filename = invoice.generate_pdf()
        json_filename = invoice.save_invoice_data()
        
        print(f"\n✅ Invoice generated successfully!")
        print(f"📄 PDF file: {pdf_filename}")
        print(f"💾 Data file: {json_filename}")
        
        # Display totals
        totals = invoice.calculate_totals()
        print(f"\n💰 Invoice Summary:")
        print(f"   Subtotal: ${totals['subtotal']:.2f}")
        if discount > 0:
            print(f"   Discount: -${totals['discount_amount']:.2f}")
        if tax_rate > 0:
            print(f"   Tax: ${totals['tax_amount']:.2f}")
        print(f"   TOTAL: ${totals['total']:.2f}")
        
    except Exception as e:
        print(f"❌ Error creating invoice: {str(e)}")

def launch_gui():
    """Launch GUI interface"""
    try:
        print("\n🖥️  Launching GUI interface...")
        from invoice_gui import main as gui_main
        gui_main()
    except ImportError:
        print("❌ GUI dependencies not available. Please install tkinter.")
    except Exception as e:
        print(f"❌ Error launching GUI: {str(e)}")

def launch_web():
    """Launch web interface"""
    try:
        print("\n🌐 Launching web interface...")
        print("📱 Access the application at: http://localhost:5000")
        print("🔄 Press Ctrl+C to stop the server")
        print()
        from web_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Web interface dependencies not available. Please install Flask.")
    except Exception as e:
        print(f"❌ Error launching web interface: {str(e)}")

def export_invoice_csv():
    """Export specific invoice to CSV"""
    exporter = InvoiceExporter()
    invoices = exporter.get_all_invoices()
    
    if not invoices:
        print("❌ No invoices found!")
        return
    
    print(f"\n📊 Available invoices: {', '.join(invoices)}")
    invoice_number = input("Enter invoice number to export: ").strip()
    
    if invoice_number not in invoices:
        print("❌ Invoice not found!")
        return
    
    try:
        invoice_data = exporter.load_invoice_from_json(invoice_number)
        if invoice_data:
            csv_file = exporter.export_to_csv(invoice_data)
            print(f"✅ Invoice exported to: {csv_file}")
        else:
            print("❌ Failed to load invoice data!")
    except Exception as e:
        print(f"❌ Error exporting invoice: {str(e)}")

def export_all_invoices():
    """Export all invoices summary"""
    try:
        exporter = InvoiceExporter()
        csv_file = exporter.export_all_invoices_to_csv()
        
        if csv_file:
            print(f"✅ All invoices exported to: {csv_file}")
        else:
            print("❌ No invoices found to export!")
    except Exception as e:
        print(f"❌ Error exporting invoices: {str(e)}")

def send_invoice_email():
    """Send invoice via email"""
    exporter = InvoiceExporter()
    invoices = exporter.get_all_invoices()
    
    if not invoices:
        print("❌ No invoices found!")
        return
    
    print(f"\n📧 Available invoices: {', '.join(invoices)}")
    invoice_number = input("Enter invoice number to send: ").strip()
    
    if invoice_number not in invoices:
        print("❌ Invoice not found!")
        return
    
    try:
        # Get email details
        print("\n📧 Email Configuration:")
        sender_email = input("Your email address: ").strip()
        sender_password = input("Your email password: ").strip()
        recipient_email = input("Recipient email address: ").strip()
        
        if not all([sender_email, sender_password, recipient_email]):
            print("❌ All email fields are required!")
            return
        
        # Load invoice data
        invoice_data = exporter.load_invoice_from_json(invoice_number)
        if not invoice_data:
            print("❌ Failed to load invoice data!")
            return
        
        # Send email
        email_sender = EmailSender()
        pdf_path = f"invoices/invoice_{invoice_number}.pdf"
        
        success, message = email_sender.send_invoice_email(
            sender_email, sender_password, recipient_email,
            pdf_path, invoice_number,
            invoice_data['client_info']['name'],
            invoice_data['business_info']['name']
        )
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

def view_invoices():
    """View existing invoices"""
    exporter = InvoiceExporter()
    invoices = exporter.get_all_invoices()
    
    if not invoices:
        print("❌ No invoices found!")
        return
    
    print(f"\n📋 Found {len(invoices)} invoices:")
    print("-" * 40)
    
    for invoice_number in invoices:
        try:
            invoice_data = exporter.load_invoice_from_json(invoice_number)
            if invoice_data:
                totals = invoice_data['totals']
                print(f"📄 Invoice #{invoice_number}")
                print(f"   Date: {invoice_data['invoice_date']}")
                print(f"   Client: {invoice_data['client_info']['name']}")
                print(f"   Total: ${totals['total']:.2f}")
                print(f"   Items: {len(invoice_data['items'])}")
                print()
        except Exception as e:
            print(f"❌ Error reading invoice {invoice_number}: {str(e)}")

def main():
    """Main application entry point"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            create_cli_invoice()
        elif choice == '2':
            launch_gui()
        elif choice == '3':
            launch_web()
        elif choice == '4':
            export_invoice_csv()
        elif choice == '5':
            export_all_invoices()
        elif choice == '6':
            send_invoice_email()
        elif choice == '7':
            view_invoices()
        elif choice == '8':
            print("\n👋 Thank you for using Professional Invoice Generator!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
