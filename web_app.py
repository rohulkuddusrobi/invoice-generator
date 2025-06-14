from flask import Flask, request, jsonify, render_template, send_file, flash, redirect, url_for
from flask_cors import CORS
import os
import json
from datetime import datetime
from invoice_generator import InvoiceGenerator
from invoice_exporter import InvoiceExporter
from email_sender import EmailSender

app = Flask(__name__)
app.secret_key = 'invoice_generator_secret_key_2025'
CORS(app)

# Ensure required directories exist
os.makedirs('invoices', exist_ok=True)
os.makedirs('exports', exist_ok=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/create')
def create_invoice_page():
    """Create invoice page"""
    return render_template('create_invoice.html')

@app.route('/view')
def view_invoices_page():
    """View invoices page"""
    exporter = InvoiceExporter()
    invoices = []
    
    try:
        invoice_numbers = exporter.get_all_invoices()
        for invoice_number in invoice_numbers:
            invoice_data = exporter.load_invoice_from_json(invoice_number)
            if invoice_data:
                invoices.append({
                    'number': invoice_number,
                    'date': invoice_data['invoice_date'],
                    'client': invoice_data['client_info']['name'],
                    'total': invoice_data['totals']['total'],
                    'items_count': len(invoice_data['items'])
                })
    except Exception as e:
        flash(f'Error loading invoices: {str(e)}', 'error')
    
    return render_template('view_invoices.html', invoices=invoices)

@app.route('/api/create-invoice', methods=['POST'])
def api_create_invoice():
    """API endpoint to create invoice"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['business_name', 'client_name', 'invoice_number', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        if not data['items']:
            return jsonify({'success': False, 'error': 'At least one item is required'}), 400
        
        # Create invoice
        invoice = InvoiceGenerator()
        
        # Set business info
        invoice.set_business_info(
            name=data['business_name'],
            address=data.get('business_address', ''),
            phone=data.get('business_phone', ''),
            email=data.get('business_email', '')
        )
        
        # Set client info
        invoice.set_client_info(
            name=data['client_name'],
            address=data.get('client_address', ''),
            phone=data.get('client_phone', ''),
            email=data.get('client_email', '')
        )
        
        # Set invoice details
        invoice.set_invoice_details(
            invoice_number=data['invoice_number'],
            invoice_date=data.get('invoice_date', datetime.now().strftime('%Y-%m-%d')),
            tax_rate=float(data.get('tax_rate', 0)),
            discount=float(data.get('discount', 0)),
            payment_terms=data.get('payment_terms', '')
        )
        
        # Add items
        for item in data['items']:
            invoice.add_item(
                description=item['description'],
                quantity=float(item['quantity']),
                unit_price=float(item['unit_price'])
            )
        
        # Generate PDF and JSON
        pdf_filename = invoice.generate_pdf()
        json_filename = invoice.save_invoice_data()
        
        # Get totals
        totals = invoice.calculate_totals()
        
        return jsonify({
            'success': True,
            'message': 'Invoice created successfully!',
            'pdf_filename': pdf_filename,
            'json_filename': json_filename,
            'totals': totals
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-invoice/<invoice_number>')
def api_get_invoice(invoice_number):
    """API endpoint to get invoice data"""
    try:
        exporter = InvoiceExporter()
        invoice_data = exporter.load_invoice_from_json(invoice_number)
        
        if invoice_data:
            return jsonify({'success': True, 'data': invoice_data})
        else:
            return jsonify({'success': False, 'error': 'Invoice not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-csv/<invoice_number>')
def api_export_csv(invoice_number):
    """API endpoint to export invoice as CSV"""
    try:
        exporter = InvoiceExporter()
        invoice_data = exporter.load_invoice_from_json(invoice_number)
        
        if not invoice_data:
            return jsonify({'success': False, 'error': 'Invoice not found'}), 404
        
        csv_filename = exporter.export_to_csv(invoice_data)
        return send_file(csv_filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-pdf/<invoice_number>')
def api_download_pdf(invoice_number):
    """API endpoint to download PDF"""
    try:
        pdf_path = f'invoices/invoice_{invoice_number}.pdf'
        if os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'PDF not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send-email', methods=['POST'])
def api_send_email():
    """API endpoint to send invoice via email"""
    try:
        data = request.get_json()
        
        print(f"📧 Email API called with data: {data}")
        
        required_fields = ['invoice_number', 'sender_email', 'sender_password', 'recipient_email']
        for field in required_fields:
            if not data.get(field):
                error_msg = f'{field} is required'
                print(f"❌ Validation error: {error_msg}")
                return jsonify({'success': False, 'error': error_msg}), 400
        
        # Load invoice data
        print(f"📄 Loading invoice data for: {data['invoice_number']}")
        exporter = InvoiceExporter()
        invoice_data = exporter.load_invoice_from_json(data['invoice_number'])
        
        if not invoice_data:
            error_msg = 'Invoice not found'
            print(f"❌ {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 404
        
        # Prepare email data
        email_sender = EmailSender()
        pdf_path = f"invoices/invoice_{data['invoice_number']}.pdf"
        
        print(f"📁 PDF path: {pdf_path}")
        print(f"📁 PDF exists: {os.path.exists(pdf_path)}")
        
        # Get optional fields
        email_subject = data.get('email_subject', None)
        email_message = data.get('email_message', None)
        
        print(f"📧 Sending email...")
        print(f"   From: {data['sender_email']}")
        print(f"   To: {data['recipient_email']}")
        print(f"   Subject: {email_subject}")
        
        # Send email
        success, message = email_sender.send_invoice_email(
            sender_email=data['sender_email'],
            sender_password=data['sender_password'],
            recipient_email=data['recipient_email'],
            invoice_pdf_path=pdf_path,
            invoice_number=data['invoice_number'],
            client_name=invoice_data['client_info']['name'],
            business_name=invoice_data['business_info']['name'],
            email_subject=email_subject,
            email_message=email_message
        )
        
        if success:
            print(f"✅ Email sent successfully!")
        else:
            print(f"❌ Email failed: {message}")
        
        return jsonify({'success': success, 'message': message})
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Email API error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/api/get-all-invoices')
def api_get_all_invoices():
    """API endpoint to get all invoices summary"""
    try:
        exporter = InvoiceExporter()
        invoices = []
        
        invoice_numbers = exporter.get_all_invoices()
        for invoice_number in invoice_numbers:
            invoice_data = exporter.load_invoice_from_json(invoice_number)
            if invoice_data:
                invoices.append({
                    'number': invoice_number,
                    'date': invoice_data['invoice_date'],
                    'client': invoice_data['client_info']['name'],
                    'total': invoice_data['totals']['total'],
                    'items_count': len(invoice_data['items'])
                })
        
        return jsonify({'success': True, 'invoices': invoices})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test-email', methods=['POST'])
def api_test_email():
    """API endpoint to test email connection"""
    try:
        data = request.get_json()
        
        required_fields = ['sender_email', 'sender_password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        print(f"🧪 Testing email connection for: {data['sender_email']}")
        
        # Test email connection
        email_sender = EmailSender()
        success, message = email_sender.test_email_connection(
            sender_email=data['sender_email'],
            sender_password=data['sender_password']
        )
        
        return jsonify({'success': success, 'message': message})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting Invoice Generator Web Interface...")
    print("📱 Access the application at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
