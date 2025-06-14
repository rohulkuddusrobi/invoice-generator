import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from invoice_generator import InvoiceGenerator

class InvoiceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Invoice Generator")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        self.invoice = InvoiceGenerator()
        self.items = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Professional Invoice Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Business Information Section
        business_frame = ttk.LabelFrame(main_frame, text="Business Information", padding="10")
        business_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        business_frame.columnconfigure(1, weight=1)
        
        ttk.Label(business_frame, text="Business Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.business_name = ttk.Entry(business_frame, width=40)
        self.business_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(business_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.business_address = ttk.Entry(business_frame, width=40)
        self.business_address.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(business_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.business_phone = ttk.Entry(business_frame, width=40)
        self.business_phone.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(business_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.business_email = ttk.Entry(business_frame, width=40)
        self.business_email.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Client Information Section
        client_frame = ttk.LabelFrame(main_frame, text="Client Information", padding="10")
        client_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        client_frame.columnconfigure(1, weight=1)
        
        ttk.Label(client_frame, text="Client Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.client_name = ttk.Entry(client_frame, width=40)
        self.client_name.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(client_frame, text="Address:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.client_address = ttk.Entry(client_frame, width=40)
        self.client_address.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(client_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.client_phone = ttk.Entry(client_frame, width=40)
        self.client_phone.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(client_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.client_email = ttk.Entry(client_frame, width=40)
        self.client_email.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Invoice Details Section
        invoice_frame = ttk.LabelFrame(main_frame, text="Invoice Details", padding="10")
        invoice_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        invoice_frame.columnconfigure(1, weight=1)
        invoice_frame.columnconfigure(3, weight=1)
        
        ttk.Label(invoice_frame, text="Invoice Number:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.invoice_number = ttk.Entry(invoice_frame, width=20)
        self.invoice_number.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=2)
        
        ttk.Label(invoice_frame, text="Date:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.invoice_date = ttk.Entry(invoice_frame, width=20)
        self.invoice_date.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2)
        self.invoice_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(invoice_frame, text="Tax Rate (%):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.tax_rate = ttk.Entry(invoice_frame, width=20)
        self.tax_rate.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20), pady=2)
        self.tax_rate.insert(0, "0")
        
        ttk.Label(invoice_frame, text="Discount (%):").grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        self.discount = ttk.Entry(invoice_frame, width=20)
        self.discount.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=2)
        self.discount.insert(0, "0")
        
        ttk.Label(invoice_frame, text="Payment Terms:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.payment_terms = ttk.Entry(invoice_frame, width=50)
        self.payment_terms.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        # Items Section
        items_frame = ttk.LabelFrame(main_frame, text="Items/Services", padding="10")
        items_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        items_frame.columnconfigure(0, weight=1)
        items_frame.rowconfigure(1, weight=1)
        
        # Item input frame
        item_input_frame = ttk.Frame(items_frame)
        item_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        item_input_frame.columnconfigure(0, weight=2)
        item_input_frame.columnconfigure(1, weight=1)
        item_input_frame.columnconfigure(2, weight=1)
        
        ttk.Label(item_input_frame, text="Description:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(item_input_frame, text="Quantity:").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Label(item_input_frame, text="Unit Price:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        self.item_description = ttk.Entry(item_input_frame, width=30)
        self.item_description.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        self.item_quantity = ttk.Entry(item_input_frame, width=10)
        self.item_quantity.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        self.item_price = ttk.Entry(item_input_frame, width=10)
        self.item_price.grid(row=1, column=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Add item button
        add_button = ttk.Button(item_input_frame, text="Add Item", command=self.add_item)
        add_button.grid(row=1, column=3, padx=(10, 0), pady=2)
        
        # Items list
        self.items_tree = ttk.Treeview(items_frame, columns=('Description', 'Quantity', 'Price', 'Total'), 
                                      show='headings', height=6)
        self.items_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns
        self.items_tree.heading('Description', text='Description')
        self.items_tree.heading('Quantity', text='Quantity')
        self.items_tree.heading('Price', text='Unit Price')
        self.items_tree.heading('Total', text='Total')
        
        self.items_tree.column('Description', width=300)
        self.items_tree.column('Quantity', width=80)
        self.items_tree.column('Price', width=100)
        self.items_tree.column('Total', width=100)
        
        # Scrollbar for items list
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        # Remove item button
        remove_button = ttk.Button(items_frame, text="Remove Selected", command=self.remove_item)
        remove_button.grid(row=2, column=0, pady=(5, 0), sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        generate_button = ttk.Button(buttons_frame, text="Generate Invoice", 
                                   command=self.generate_invoice, style='Accent.TButton')
        generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(buttons_frame, text="Clear All", command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        # Configure main frame row weights
        main_frame.rowconfigure(4, weight=1)
        
    def add_item(self):
        """Add item to the list"""
        description = self.item_description.get().strip()
        quantity_str = self.item_quantity.get().strip()
        price_str = self.item_price.get().strip()
        
        if not description or not quantity_str or not price_str:
            messagebox.showerror("Error", "Please fill in all item fields")
            return
        
        try:
            quantity = float(quantity_str)
            price = float(price_str)
            total = quantity * price
            
            # Add to tree view
            self.items_tree.insert('', 'end', values=(description, quantity, f"${price:.2f}", f"${total:.2f}"))
            
            # Add to items list
            self.items.append({
                'description': description,
                'quantity': quantity,
                'unit_price': price,
                'total_price': total
            })
            
            # Clear input fields
            self.item_description.delete(0, tk.END)
            self.item_quantity.delete(0, tk.END)
            self.item_price.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Quantity and Price must be valid numbers")
    
    def remove_item(self):
        """Remove selected item from the list"""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        # Get the index of the selected item
        index = self.items_tree.index(selected[0])
        
        # Remove from tree view
        self.items_tree.delete(selected[0])
        
        # Remove from items list
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def generate_invoice(self):
        """Generate the invoice PDF"""
        # Validate required fields
        if not self.business_name.get().strip():
            messagebox.showerror("Error", "Business name is required")
            return
        
        if not self.client_name.get().strip():
            messagebox.showerror("Error", "Client name is required")
            return
        
        if not self.invoice_number.get().strip():
            messagebox.showerror("Error", "Invoice number is required")
            return
        
        if not self.items:
            messagebox.showerror("Error", "Please add at least one item")
            return
        
        try:
            # Set business info
            self.invoice.set_business_info(
                self.business_name.get(),
                self.business_address.get(),
                self.business_phone.get(),
                self.business_email.get()
            )
            
            # Set client info
            self.invoice.set_client_info(
                self.client_name.get(),
                self.client_address.get(),
                self.client_phone.get(),
                self.client_email.get()
            )
            
            # Set invoice details
            tax_rate = float(self.tax_rate.get() or "0")
            discount = float(self.discount.get() or "0")
            
            self.invoice.set_invoice_details(
                self.invoice_number.get(),
                self.invoice_date.get(),
                tax_rate,
                discount,
                self.payment_terms.get()
            )
            
            # Add items
            self.invoice.items = self.items.copy()
            
            # Generate PDF
            pdf_filename = self.invoice.generate_pdf()
            json_filename = self.invoice.save_invoice_data()
            
            # Show success message
            totals = self.invoice.calculate_totals()
            message = f"Invoice generated successfully!\n\n"
            message += f"PDF: {pdf_filename}\n"
            message += f"Data: {json_filename}\n\n"
            message += f"Total Amount: ${totals['total']:.2f}"
            
            messagebox.showinfo("Success", message)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Please enter valid numbers for tax rate and discount: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")
    
    def clear_all(self):
        """Clear all fields"""
        # Clear business info
        self.business_name.delete(0, tk.END)
        self.business_address.delete(0, tk.END)
        self.business_phone.delete(0, tk.END)
        self.business_email.delete(0, tk.END)
        
        # Clear client info
        self.client_name.delete(0, tk.END)
        self.client_address.delete(0, tk.END)
        self.client_phone.delete(0, tk.END)
        self.client_email.delete(0, tk.END)
        
        # Clear invoice details
        self.invoice_number.delete(0, tk.END)
        self.invoice_date.delete(0, tk.END)
        self.invoice_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tax_rate.delete(0, tk.END)
        self.tax_rate.insert(0, "0")
        self.discount.delete(0, tk.END)
        self.discount.insert(0, "0")
        self.payment_terms.delete(0, tk.END)
        
        # Clear item inputs
        self.item_description.delete(0, tk.END)
        self.item_quantity.delete(0, tk.END)
        self.item_price.delete(0, tk.END)
        
        # Clear items list
        self.items_tree.delete(*self.items_tree.get_children())
        self.items.clear()


def main():
    root = tk.Tk()
    app = InvoiceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
