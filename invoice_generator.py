from fpdf import FPDF
from datetime import datetime
import os
import json

class InvoiceGenerator:
    def __init__(self):
        self.business_info = {}
        self.client_info = {}
        self.items = []
        self.invoice_number = ""
        self.invoice_date = datetime.now().strftime("%Y-%m-%d")
        self.tax_rate = 0.0
        self.discount = 0.0
        self.payment_terms = ""
        
    def set_business_info(self, name, address, phone, email=""):
        """Set business information"""
        self.business_info = {
            'name': name,
            'address': address,
            'phone': phone,
            'email': email
        }
    
    def set_client_info(self, name, address, phone="", email=""):
        """Set client information"""
        self.client_info = {
            'name': name,
            'address': address,
            'phone': phone,
            'email': email
        }
    
    def add_item(self, description, quantity, unit_price):
        """Add an item to the invoice"""
        total_price = quantity * unit_price
        self.items.append({
            'description': description,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price
        })
    
    def set_invoice_details(self, invoice_number, invoice_date=None, tax_rate=0.0, discount=0.0, payment_terms=""):
        """Set invoice details"""
        self.invoice_number = invoice_number
        if invoice_date:
            self.invoice_date = invoice_date
        self.tax_rate = tax_rate
        self.discount = discount
        self.payment_terms = payment_terms
    
    def calculate_totals(self):
        """Calculate subtotal, tax, discount, and total"""
        subtotal = sum(item['total_price'] for item in self.items)
        discount_amount = subtotal * (self.discount / 100)
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * (self.tax_rate / 100)
        total = taxable_amount + tax_amount
        
        return {
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'total': total
        }
    
    def generate_pdf(self):
        """Generate PDF invoice"""
        # Create invoices directory if it doesn't exist
        if not os.path.exists('invoices'):
            os.makedirs('invoices')
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Header - Business Info
        pdf.cell(0, 10, 'INVOICE', 0, 1, 'C')
        pdf.ln(10)
        
        # Business Information
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, self.business_info['name'], 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, self.business_info['address'], 0, 1)
        pdf.cell(0, 6, f"Phone: {self.business_info['phone']}", 0, 1)
        if self.business_info['email']:
            pdf.cell(0, 6, f"Email: {self.business_info['email']}", 0, 1)
        
        pdf.ln(10)
        
        # Invoice details and Client info side by side
        pdf.set_font('Arial', 'B', 10)
        
        # Left side - Invoice Details
        pdf.cell(95, 6, f"Invoice Number: {self.invoice_number}", 0, 0)
        # Right side - Bill To
        pdf.cell(95, 6, "BILL TO:", 0, 1)
        
        pdf.set_font('Arial', '', 10)
        pdf.cell(95, 6, f"Invoice Date: {self.invoice_date}", 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(95, 6, self.client_info['name'], 0, 1)
        
        pdf.set_font('Arial', '', 10)
        pdf.cell(95, 6, "", 0, 0)  # Empty cell for alignment
        pdf.cell(95, 6, self.client_info['address'], 0, 1)
        
        if self.client_info['phone']:
            pdf.cell(95, 6, "", 0, 0)  # Empty cell for alignment
            pdf.cell(95, 6, f"Phone: {self.client_info['phone']}", 0, 1)
        
        if self.client_info['email']:
            pdf.cell(95, 6, "", 0, 0)  # Empty cell for alignment
            pdf.cell(95, 6, f"Email: {self.client_info['email']}", 0, 1)
        
        pdf.ln(10)
        
        # Items table header
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(80, 8, 'Description', 1, 0, 'C')
        pdf.cell(25, 8, 'Quantity', 1, 0, 'C')
        pdf.cell(30, 8, 'Unit Price', 1, 0, 'C')
        pdf.cell(30, 8, 'Total', 1, 1, 'C')
        
        # Items
        pdf.set_font('Arial', '', 9)
        for item in self.items:
            pdf.cell(80, 8, item['description'], 1, 0)
            pdf.cell(25, 8, str(item['quantity']), 1, 0, 'C')
            pdf.cell(30, 8, f"${item['unit_price']:.2f}", 1, 0, 'R')
            pdf.cell(30, 8, f"${item['total_price']:.2f}", 1, 1, 'R')
        
        # Totals
        totals = self.calculate_totals()
        pdf.ln(5)
        
        # Right-aligned totals
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(135, 8, 'Subtotal:', 0, 0, 'R')
        pdf.cell(30, 8, f"${totals['subtotal']:.2f}", 1, 1, 'R')
        
        if self.discount > 0:
            pdf.cell(135, 8, f'Discount ({self.discount}%):', 0, 0, 'R')
            pdf.cell(30, 8, f"-${totals['discount_amount']:.2f}", 1, 1, 'R')
        
        if self.tax_rate > 0:
            pdf.cell(135, 8, f'Tax ({self.tax_rate}%):', 0, 0, 'R')
            pdf.cell(30, 8, f"${totals['tax_amount']:.2f}", 1, 1, 'R')
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(135, 10, 'TOTAL:', 0, 0, 'R')
        pdf.cell(30, 10, f"${totals['total']:.2f}", 1, 1, 'R')
        
        # Payment terms
        if self.payment_terms:
            pdf.ln(10)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 8, 'Payment Terms:', 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, self.payment_terms, 0, 1)
        
        # Footer
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 6, 'Thank you for your business!', 0, 1, 'C')
        
        # Save PDF
        filename = f"invoices/invoice_{self.invoice_number}.pdf"
        pdf.output(filename)
        return filename
    
    def save_invoice_data(self):
        """Save invoice data to JSON file"""
        data = {
            'business_info': self.business_info,
            'client_info': self.client_info,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date,
            'items': self.items,
            'tax_rate': self.tax_rate,
            'discount': self.discount,
            'payment_terms': self.payment_terms,
            'totals': self.calculate_totals()
        }
        
        filename = f"invoices/invoice_{self.invoice_number}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename


def main():
    """Main function to run the invoice generator"""
    print("=== Professional Invoice Generator ===")
    print()
    
    # Create invoice generator instance
    invoice = InvoiceGenerator()
    
    # Get business information
    print("Enter Business Information:")
    business_name = input("Business Name: ")
    business_address = input("Business Address: ")
    business_phone = input("Business Phone: ")
    business_email = input("Business Email (optional): ")
    
    invoice.set_business_info(business_name, business_address, business_phone, business_email)
    
    print("\nEnter Client Information:")
    client_name = input("Client Name: ")
    client_address = input("Client Address: ")
    client_phone = input("Client Phone (optional): ")
    client_email = input("Client Email (optional): ")
    
    invoice.set_client_info(client_name, client_address, client_phone, client_email)
    
    # Get invoice details
    print("\nEnter Invoice Details:")
    invoice_number = input("Invoice Number: ")
    invoice_date = input("Invoice Date (YYYY-MM-DD) or press Enter for today: ")
    if not invoice_date:
        invoice_date = datetime.now().strftime("%Y-%m-%d")
    
    tax_rate = input("Tax Rate (%) or press Enter for 0: ")
    if not tax_rate:
        tax_rate = 0.0
    else:
        tax_rate = float(tax_rate)
    
    discount = input("Discount (%) or press Enter for 0: ")
    if not discount:
        discount = 0.0
    else:
        discount = float(discount)
    
    payment_terms = input("Payment Terms (optional): ")
    
    invoice.set_invoice_details(invoice_number, invoice_date, tax_rate, discount, payment_terms)
    
    # Get items
    print("\nEnter Items/Services:")
    while True:
        description = input("Item Description (or 'done' to finish): ")
        if description.lower() == 'done':
            break
            
        quantity = float(input("Quantity: "))
        unit_price = float(input("Unit Price: $"))
        
        invoice.add_item(description, quantity, unit_price)
        print(f"Added: {description} - Qty: {quantity} - Price: ${unit_price:.2f}")
        print()
    
    # Generate invoice
    try:
        print("\nGenerating invoice...")
        pdf_filename = invoice.generate_pdf()
        json_filename = invoice.save_invoice_data()
        
        print(f"✅ Invoice PDF generated: {pdf_filename}")
        print(f"✅ Invoice data saved: {json_filename}")
        
        # Display totals
        totals = invoice.calculate_totals()
        print(f"\n=== Invoice Summary ===")
        print(f"Subtotal: ${totals['subtotal']:.2f}")
        if discount > 0:
            print(f"Discount: -${totals['discount_amount']:.2f}")
        if tax_rate > 0:
            print(f"Tax: ${totals['tax_amount']:.2f}")
        print(f"TOTAL: ${totals['total']:.2f}")
        
    except Exception as e:
        print(f"❌ Error generating invoice: {str(e)}")


if __name__ == "__main__":
    main()
