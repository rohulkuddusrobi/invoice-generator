Build a professional Invoice Generator application using Python.

🔧 Technologies to use:
- Python as the core language
- fpdf2 library to generate PDF invoices
- datetime to generate invoice dates
- os for saving invoices into folders
- tkinter (optional) for a GUI interface

🎯 Features to include:
1. Accept user input for:
   - Business name, address, phone number
   - Client name and address
   - List of products/services: each with description, quantity, unit price
   - Invoice date (default to today)
   - Invoice number (auto-generate or manual)
   - Tax or discount (optional)
   - Payment terms or method (e.g., Bank, Cash, bKash)

2. Calculate:
   - Total price per item (quantity × price)
   - Subtotal
   - Discount/tax if any
   - Final total

3. Generate a clean, professional PDF with:
   - Business logo (optional)
   - Header: Business info
   - Client section
   - Table for item list
   - Totals at the bottom
   - Footer: Thank you note or payment terms

4. Save the PDF invoice into a folder named `/invoices` with the filename pattern:
   `invoice_<invoice_number>.pdf`

5. Optional (Advanced):
   - GUI version using `tkinter`
   - Export invoice data to `.json` or `.csv`
   - Email the invoice as an attachment using `smtplib`

📁 File Structure:
- `invoice_generator.py` — main script
- `/invoices` — folder where PDFs will be stored
- `logo.png` — optional logo for the invoice
- `requirements.txt` — for installing `fpdf2`

📦 Required Installation:
```bash
pip install fpdf2
