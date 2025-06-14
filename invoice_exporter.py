import csv
import json
import os
from datetime import datetime

class InvoiceExporter:
    def __init__(self):
        self.invoices_dir = "invoices"
        self.exports_dir = "exports"
        
        # Create exports directory if it doesn't exist
        if not os.path.exists(self.exports_dir):
            os.makedirs(self.exports_dir)
    
    def export_to_csv(self, invoice_data, filename=None):
        """Export invoice data to CSV format"""
        if filename is None:
            filename = f"invoice_{invoice_data['invoice_number']}.csv"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header information
            writer.writerow(['Invoice Export'])
            writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Business information
            writer.writerow(['Business Information'])
            writer.writerow(['Name:', invoice_data['business_info']['name']])
            writer.writerow(['Address:', invoice_data['business_info']['address']])
            writer.writerow(['Phone:', invoice_data['business_info']['phone']])
            writer.writerow(['Email:', invoice_data['business_info']['email']])
            writer.writerow([])
            
            # Client information
            writer.writerow(['Client Information'])
            writer.writerow(['Name:', invoice_data['client_info']['name']])
            writer.writerow(['Address:', invoice_data['client_info']['address']])
            writer.writerow(['Phone:', invoice_data['client_info']['phone']])
            writer.writerow(['Email:', invoice_data['client_info']['email']])
            writer.writerow([])
            
            # Invoice details
            writer.writerow(['Invoice Details'])
            writer.writerow(['Invoice Number:', invoice_data['invoice_number']])
            writer.writerow(['Invoice Date:', invoice_data['invoice_date']])
            writer.writerow(['Tax Rate (%):', invoice_data['tax_rate']])
            writer.writerow(['Discount (%):', invoice_data['discount']])
            writer.writerow(['Payment Terms:', invoice_data['payment_terms']])
            writer.writerow([])
            
            # Items header
            writer.writerow(['Items'])
            writer.writerow(['Description', 'Quantity', 'Unit Price', 'Total Price'])
            
            # Items data
            for item in invoice_data['items']:
                writer.writerow([
                    item['description'],
                    item['quantity'],
                    f"${item['unit_price']:.2f}",
                    f"${item['total_price']:.2f}"
                ])
            
            writer.writerow([])
            
            # Totals
            totals = invoice_data['totals']
            writer.writerow(['Summary'])
            writer.writerow(['Subtotal:', f"${totals['subtotal']:.2f}"])
            if totals['discount_amount'] > 0:
                writer.writerow(['Discount:', f"-${totals['discount_amount']:.2f}"])
            if totals['tax_amount'] > 0:
                writer.writerow(['Tax:', f"${totals['tax_amount']:.2f}"])
            writer.writerow(['Total:', f"${totals['total']:.2f}"])
        
        return filepath
    
    def export_all_invoices_to_csv(self):
        """Export all invoices to a single CSV file"""
        all_invoices = []
        
        # Read all JSON files in invoices directory
        if os.path.exists(self.invoices_dir):
            for filename in os.listdir(self.invoices_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.invoices_dir, filename)
                    with open(filepath, 'r') as f:
                        invoice_data = json.load(f)
                        all_invoices.append(invoice_data)
        
        if not all_invoices:
            return None
        
        # Create summary CSV
        summary_filepath = os.path.join(self.exports_dir, f"all_invoices_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        with open(summary_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                'Invoice Number', 'Invoice Date', 'Client Name', 'Client Address',
                'Subtotal', 'Tax Amount', 'Discount Amount', 'Total', 'Payment Terms'
            ])
            
            # Write invoice data
            for invoice in all_invoices:
                totals = invoice['totals']
                writer.writerow([
                    invoice['invoice_number'],
                    invoice['invoice_date'],
                    invoice['client_info']['name'],
                    invoice['client_info']['address'],
                    f"${totals['subtotal']:.2f}",
                    f"${totals['tax_amount']:.2f}",
                    f"${totals['discount_amount']:.2f}",
                    f"${totals['total']:.2f}",
                    invoice['payment_terms']
                ])
        
        return summary_filepath
    
    def load_invoice_from_json(self, invoice_number):
        """Load invoice data from JSON file"""
        filepath = os.path.join(self.invoices_dir, f"invoice_{invoice_number}.json")
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            return None
    
    def get_all_invoices(self):
        """Get list of all invoice numbers"""
        invoices = []
        
        if os.path.exists(self.invoices_dir):
            for filename in os.listdir(self.invoices_dir):
                if filename.endswith('.json'):
                    # Extract invoice number from filename
                    invoice_number = filename.replace('invoice_', '').replace('.json', '')
                    invoices.append(invoice_number)
        
        return sorted(invoices)


# Example usage and testing
if __name__ == "__main__":
    exporter = InvoiceExporter()
    
    # Get all invoices
    invoices = exporter.get_all_invoices()
    print(f"Found {len(invoices)} invoices: {invoices}")
    
    # Export all invoices summary
    if invoices:
        summary_file = exporter.export_all_invoices_to_csv()
        if summary_file:
            print(f"Summary exported to: {summary_file}")
        else:
            print("No invoices found to export")
    else:
        print("No invoices found")
