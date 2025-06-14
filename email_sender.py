import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
        # Setup logging for debugging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def send_invoice_email(self, sender_email, sender_password, recipient_email, 
                          invoice_pdf_path, invoice_number, client_name, business_name,
                          email_subject=None, email_message=None):
        """Send invoice as email attachment with enhanced debugging"""
        
        try:
            self.logger.info(f"📧 Starting email send process...")
            self.logger.info(f"   From: {sender_email}")
            self.logger.info(f"   To: {recipient_email}")
            self.logger.info(f"   Invoice: {invoice_number}")
            self.logger.info(f"   PDF Path: {invoice_pdf_path}")
            
            # Check if PDF file exists
            if not os.path.exists(invoice_pdf_path):
                error_msg = f"Invoice PDF file not found: {invoice_pdf_path}"
                self.logger.error(f"❌ {error_msg}")
                return False, error_msg
            
            # Get file size for logging
            file_size = os.path.getsize(invoice_pdf_path)
            self.logger.info(f"   PDF Size: {file_size} bytes")
            
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # Use custom subject or default
            if email_subject:
                msg['Subject'] = email_subject
            else:
                msg['Subject'] = f"Invoice #{invoice_number} from {business_name}"
            
            self.logger.info(f"   Subject: {msg['Subject']}")
            
            # Email body - use custom message or default
            if email_message:
                body = email_message
            else:
                body = f"""Dear {client_name},

Thank you for your business! Please find attached invoice #{invoice_number}.

Invoice Details:
- Invoice Number: {invoice_number}
- Business: {business_name}

If you have any questions about this invoice, please don't hesitate to contact us.

Best regards,
{business_name}
{sender_email}"""
            
            msg.attach(MIMEText(body, 'plain'))
            self.logger.info(f"   Message attached")
            
            # Attach PDF file
            with open(invoice_pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename=invoice_{invoice_number}.pdf'
                )
                msg.attach(part)
            
            self.logger.info(f"   PDF attachment added")
            
            # Send email with detailed logging
            self.logger.info(f"🔄 Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)  # Enable SMTP debugging
            
            self.logger.info(f"🔐 Starting TLS...")
            server.starttls()
            
            self.logger.info(f"🔑 Logging in with email: {sender_email}")
            server.login(sender_email, sender_password)
            
            self.logger.info(f"📤 Sending email...")
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            
            self.logger.info(f"🔚 Closing connection...")
            server.quit()
            
            success_msg = f"✅ Email sent successfully to {recipient_email}!"
            self.logger.info(success_msg)
            
            return True, success_msg
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"❌ Gmail Authentication Failed! Please check:\n1. Use App Password (not regular password)\n2. Enable 2-Factor Authentication\n3. Generate App Password from Google Account settings\nError: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
            
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"❌ Recipient email address rejected: {recipient_email}. Please check the email address."
            self.logger.error(error_msg)
            return False, error_msg
            
        except smtplib.SMTPServerDisconnected as e:
            error_msg = f"❌ Connection to Gmail server lost. Please check your internet connection."
            self.logger.error(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"❌ Email sending failed: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    def test_email_connection(self, sender_email, sender_password):
        """Test email connection without sending"""
        try:
            self.logger.info(f"🧪 Testing email connection for: {sender_email}")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)
            server.starttls()
            server.login(sender_email, sender_password)
            server.quit()
            
            self.logger.info(f"✅ Email connection test successful!")
            return True, "Connection successful!"
            
        except Exception as e:
            error_msg = f"❌ Connection test failed: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg


# Test script
if __name__ == "__main__":
    # Test email connection
    email_sender = EmailSender()
    
    # Test with your credentials
    test_email = "marketerrobi@gmail.com"
    test_password = "NotFound#404"
    
    print("🧪 Testing email connection...")
    success, message = email_sender.test_email_connection(test_email, test_password)
    
    if success:
        print("✅ Email connection works!")
    else:
        print(f"❌ Email connection failed: {message}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure 2-Factor Authentication is enabled")
        print("2. Generate App Password from Google Account > Security > App passwords")
        print("3. Use App Password instead of regular password")
        print("4. Check internet connection")
