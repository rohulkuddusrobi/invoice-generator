# 🧾 Professional Invoice Generator

A comprehensive, multi-interface invoice generator built with Python, featuring web, desktop, and CLI interfaces. Generate professional PDF invoices, manage client data, and send invoices via email with ease.

## ✨ Features

### 🎯 Core Features
- **PDF Invoice Generation** - Create professional, customizable PDF invoices
- **Multiple Interfaces** - Web, Desktop (Tkinter), and Command Line
- **Email Integration** - Send invoices directly via Gmail with attachment
- **Data Export** - Export invoice data to CSV and Excel formats
- **Client Management** - Store and manage client information
- **Professional Templates** - Beautiful, modern invoice templates

### 🌐 Web Interface
- **Modern UI/UX** - Professional, responsive design
- **Real-time Preview** - See invoice details before generation
- **Batch Operations** - Generate multiple invoices efficiently
- **Search & Filter** - Find invoices quickly
- **Dashboard** - Overview of invoice statistics

### 📧 Email Features
- **Gmail Integration** - Pre-configured business email setup
- **Custom Templates** - Professional email templates
- **Attachment Support** - Automatically attach PDF invoices
- **Delivery Tracking** - Track email delivery status

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rohulkuddusrobi/invoice-generator.git
   cd invoice-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   
   **Web Interface (Recommended):**
   ```bash
   python web_app.py
   ```
   Then open http://localhost:5000 in your browser
   
   **Desktop GUI:**
   ```bash
   python invoice_gui.py
   ```
   
   **Command Line:**
   ```bash
   python main.py
   ```

### 🪟 Windows Quick Setup
For Windows users, use the provided batch files:
- `install.bat` - Install dependencies
- `run_web.bat` - Start web interface
- `run.bat` - Start desktop GUI

## 📁 Project Structure

```
invoice-generator/
├── 📄 Core Files
│   ├── invoice_generator.py    # Main invoice generation logic
│   ├── web_app.py             # Flask web application
│   ├── invoice_gui.py         # Tkinter desktop GUI
│   ├── email_sender.py        # Email functionality
│   ├── invoice_exporter.py    # Data export utilities
│   └── main.py               # CLI interface
├── 🎨 Web Interface
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── create_invoice.html
│   │   └── view_invoices.html
│   └── static/              # CSS, JS, assets
│       ├── css/style.css
│       └── js/
├── 🧪 Testing
│   ├── test_invoice.py       # Core functionality tests
│   ├── test_web_api.py      # Web API tests
│   ├── test_email_functionality.py
│   └── test_gmail_setup.py
├── 📖 Documentation
│   ├── WEB_INTERFACE_GUIDE.md
│   ├── BUSINESS_EMAIL_SETUP.md
│   ├── GMAIL_SETUP_GUIDE.md
│   └── EMAIL_IMPLEMENTATION_SUMMARY.md
└── 📂 Generated Files
    ├── invoices/            # Generated PDF invoices
    └── exports/             # Exported data files
```

## 🔧 Configuration

### Email Setup
1. **Gmail App Password Setup**
   - Enable 2-factor authentication on your Gmail account
   - Generate an App Password for the application
   - See `GMAIL_SETUP_GUIDE.md` for detailed instructions

2. **Configure Email Settings**
   ```json
   {
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "sender_email": "your-business@gmail.com",
     "sender_password": "your-app-password",
     "sender_name": "Your Business Name"
   }
   ```

## 🛠️ Usage Examples

### Web Interface
1. Start the web server: `python web_app.py`
2. Open your browser to `http://localhost:5000`
3. Navigate to "Create Invoice"
4. Fill in business and client details
5. Add invoice items
6. Generate PDF and send via email

### Desktop GUI
1. Run `python invoice_gui.py`
2. Enter invoice details in the form
3. Add line items using the "Add Item" button
4. Click "Generate Invoice" to create PDF
5. Use "Send Email" to deliver the invoice

### Command Line
```bash
python main.py
# Follow the interactive prompts to create invoices
```

## 📊 Features in Detail

### Invoice Generation
- **Customizable Templates** - Professional layouts with company branding
- **Tax Calculations** - Automatic tax and discount calculations
- **Multiple Currencies** - Support for different currency formats
- **Item Management** - Add unlimited items with descriptions and pricing

### Data Management
- **JSON Storage** - Structured data storage for easy retrieval
- **Export Options** - CSV and Excel export for accounting software
- **Search Functionality** - Find invoices by client name, date, or amount
- **Backup & Recovery** - Data integrity and backup features

### Email Integration
- **SMTP Configuration** - Secure email delivery via Gmail
- **Template Customization** - Personalized email templates
- **Attachment Handling** - Automatic PDF attachment
- **Delivery Confirmation** - Track email delivery status

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Test core invoice generation
python test_invoice.py

# Test web API endpoints
python test_web_api.py

# Test email functionality
python test_email_functionality.py

# Test Gmail setup
python test_gmail_setup.py
```

## 📚 Documentation

- **[Web Interface Guide](WEB_INTERFACE_GUIDE.md)** - Complete web interface documentation
- **[Business Email Setup](BUSINESS_EMAIL_SETUP.md)** - Email configuration guide
- **[Gmail Setup Guide](GMAIL_SETUP_GUIDE.md)** - Step-by-step Gmail setup
- **[Email Implementation](EMAIL_IMPLEMENTATION_SUMMARY.md)** - Technical email details

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Security Notice

- Never commit your `email_config.json` file to version control
- Use App Passwords instead of your main Gmail password
- Keep your email credentials secure and private

## 🔧 Troubleshooting

### Common Issues

1. **Email not sending**
   - Check Gmail App Password configuration
   - Verify SMTP settings
   - Run `python test_gmail_setup.py`

2. **PDF generation fails**
   - Install required fonts
   - Check file permissions
   - Verify output directory exists

3. **Web interface not loading**
   - Check if port 5000 is available
   - Verify Flask installation
   - Check for Python errors in terminal

### Getting Help

- **Issues**: Open an issue on GitHub
- **Documentation**: Check the documentation files
- **Email**: Contact the maintainer

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] Advanced reporting and analytics
- [ ] Mobile app interface
- [ ] API documentation
- [ ] Docker containerization
- [ ] Cloud deployment guides

## 👨‍💻 Author

**Rohul Kuddus Robi**
- GitHub: [@rohulkuddusrobi](https://github.com/rohulkuddusrobi)
- Project Link: [https://github.com/rohulkuddusrobi/invoice-generator](https://github.com/rohulkuddusrobi/invoice-generator)

## 🙏 Acknowledgments

- Flask framework for the web interface
- Tkinter for the desktop GUI
- ReportLab for PDF generation
- Bootstrap for responsive design
- Font Awesome for icons

---

⭐ **Star this repository if you find it helpful!**
