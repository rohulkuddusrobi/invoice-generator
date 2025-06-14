// Create Invoice JavaScript

let items = [];
let currentInvoiceData = null;

// Initialize form
document.addEventListener('DOMContentLoaded', function() {
    // Set today's date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('invoiceDate').value = today;
    
    // Generate auto invoice number
    generateInvoiceNumber();
    
    // Auto-save form data (check if InvoiceGenerator is available)
    if (window.InvoiceGenerator && InvoiceGenerator.autoSaveForm) {
        InvoiceGenerator.autoSaveForm('invoiceForm', 'invoice_draft');
    }
    
    // Add event listeners
    setupEventListeners();
    
    // Load saved items if any
    loadSavedItems();
});

function setupEventListeners() {
    // Tax and discount change listeners
    document.getElementById('taxRate').addEventListener('input', calculateTotals);
    document.getElementById('discount').addEventListener('input', calculateTotals);
    
    // Item input enter key listener
    document.addEventListener('keypress', function(e) {
        if (e.target.closest('.row.g-3.mb-3') && e.key === 'Enter') {
            e.preventDefault();
            addItem();
        }
    });
    
    // Form submission
    document.getElementById('invoiceForm').addEventListener('submit', function(e) {
        e.preventDefault();
        generateInvoice();
    });
}

function generateInvoiceNumber() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const time = String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0');
    
    const invoiceNumber = `INV-${year}${month}${day}-${time}`;
    document.getElementById('invoiceNumber').value = invoiceNumber;
}

function addItem() {
    const description = document.getElementById('itemDescription').value.trim();
    const quantity = parseFloat(document.getElementById('itemQuantity').value) || 0;
    const price = parseFloat(document.getElementById('itemPrice').value) || 0;
    
    if (!description) {
        InvoiceGenerator.showToast('Please enter item description', 'danger');
        document.getElementById('itemDescription').focus();
        return;
    }
    
    if (quantity <= 0) {
        InvoiceGenerator.showToast('Please enter valid quantity', 'danger');
        document.getElementById('itemQuantity').focus();
        return;
    }
    
    if (price <= 0) {
        InvoiceGenerator.showToast('Please enter valid price', 'danger');
        document.getElementById('itemPrice').focus();
        return;
    }
    
    const total = quantity * price;
    const item = {
        id: Date.now(),
        description,
        quantity,
        unit_price: price,
        total_price: total
    };
    
    items.push(item);
    addItemToTable(item);
    clearItemInputs();
    calculateTotals();
    saveItems();
    
    InvoiceGenerator.showToast('Item added successfully');
}

function addItemToTable(item) {
    const tbody = document.getElementById('itemsTableBody');
    const row = document.createElement('tr');
    row.setAttribute('data-item-id', item.id);
    
    row.innerHTML = `
        <td>${item.description}</td>
        <td class="text-center">${item.quantity}</td>
        <td class="text-end">${InvoiceGenerator.formatCurrency(item.unit_price)}</td>
        <td class="text-end">${InvoiceGenerator.formatCurrency(item.total_price)}</td>
        <td class="text-center">
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeItem(${item.id})">
                <i class="fas fa-trash"></i>
            </button>
        </td>
    `;
    
    tbody.appendChild(row);
}

function removeItem(itemId) {
    items = items.filter(item => item.id !== itemId);
    
    const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
    if (row) {
        row.remove();
    }
    
    calculateTotals();
    saveItems();
    
    InvoiceGenerator.showToast('Item removed', 'warning');
}

function clearItemInputs() {
    document.getElementById('itemDescription').value = '';
    document.getElementById('itemQuantity').value = '';
    document.getElementById('itemPrice').value = '';
    document.getElementById('itemDescription').focus();
}

function calculateTotals() {
    const subtotal = items.reduce((sum, item) => sum + item.total_price, 0);
    const discountRate = parseFloat(document.getElementById('discount').value) || 0;
    const taxRate = parseFloat(document.getElementById('taxRate').value) || 0;
    
    const discountAmount = subtotal * (discountRate / 100);
    const taxableAmount = subtotal - discountAmount;
    const taxAmount = taxableAmount * (taxRate / 100);
    const grandTotal = taxableAmount + taxAmount;
    
    // Update display
    document.getElementById('subtotal').textContent = InvoiceGenerator.formatCurrency(subtotal);
    document.getElementById('discountAmount').textContent = InvoiceGenerator.formatCurrency(discountAmount);
    document.getElementById('taxAmount').textContent = InvoiceGenerator.formatCurrency(taxAmount);
    document.getElementById('grandTotal').textContent = InvoiceGenerator.formatCurrency(grandTotal);
    
    // Show/hide discount and tax rows
    document.getElementById('discountRow').style.display = discountRate > 0 ? 'table-row' : 'none';
    document.getElementById('taxRow').style.display = taxRate > 0 ? 'table-row' : 'none';
    
    return {
        subtotal,
        discountAmount,
        taxAmount,
        grandTotal
    };
}

function saveItems() {
    InvoiceGenerator.saveToLocalStorage('invoice_items', items);
}

function loadSavedItems() {
    const savedItems = InvoiceGenerator.loadFromLocalStorage('invoice_items');
    if (savedItems && Array.isArray(savedItems)) {
        items = savedItems;
        
        // Add items to table
        items.forEach(item => addItemToTable(item));
        calculateTotals();
    }
}

async function generateInvoice() {
    console.log('🚀 Starting invoice generation...');
    console.log('📊 Current items:', items);
      // Check if InvoiceGenerator is available
    if (!window.InvoiceGenerator) {
        console.error('❌ InvoiceGenerator not available');
        resetSubmitButton();
        alert('Error: InvoiceGenerator not loaded. Please refresh the page.');
        return;
    }
    console.log('✅ InvoiceGenerator is available');
    
    // Get form element
    const form = document.getElementById('invoiceForm');
    if (!form) {
        console.error('❌ Invoice form not found');
        resetSubmitButton();
        alert('Error: Invoice form not found. Please refresh the page.');
        return;
    }
    console.log('✅ Invoice form found');
      // Validate required fields
    console.log('🔍 Validating required fields...');
    if (!InvoiceGenerator.validateRequired(form)) {
        console.log('❌ Validation failed - required fields missing');
        resetSubmitButton();
        InvoiceGenerator.showToast('Please fill in all required fields', 'danger');
        return;
    }
    console.log('✅ Required fields validation passed');
    
    // Check items
    if (items.length === 0) {
        console.log('❌ No items added');
        resetSubmitButton();
        InvoiceGenerator.showToast('Please add at least one item', 'danger');
        return;
    }
    console.log(`✅ Items validation passed (${items.length} items)`);
      // Show loading modal
    console.log('📱 Showing loading modal...');
    try {
        const loadingModal = InvoiceGenerator.showLoadingModal('Generating Invoice...', 'Creating your professional invoice PDF.');
        console.log('✅ Loading modal shown');
    } catch (modalError) {
        console.error('❌ Error showing loading modal:', modalError);
        resetSubmitButton();
        alert('Error showing loading modal: ' + modalError.message);
        return;
    }
    
    try {
        console.log('📝 Preparing invoice data...');
        
        // Get form values with detailed logging
        const businessName = document.getElementById('businessName').value;
        const businessAddress = document.getElementById('businessAddress').value;
        const businessPhone = document.getElementById('businessPhone').value;
        const businessEmail = document.getElementById('businessEmail').value;
        const clientName = document.getElementById('clientName').value;
        const clientAddress = document.getElementById('clientAddress').value;
        const clientPhone = document.getElementById('clientPhone').value;
        const clientEmail = document.getElementById('clientEmail').value;
        const invoiceNumber = document.getElementById('invoiceNumber').value;
        const invoiceDate = document.getElementById('invoiceDate').value;
        const taxRate = parseFloat(document.getElementById('taxRate').value) || 0;
        const discount = parseFloat(document.getElementById('discount').value) || 0;
        const paymentTerms = document.getElementById('paymentTerms').value;
        
        console.log('📋 Form values collected:', {
            businessName, clientName, invoiceNumber, 
            itemCount: items.length, taxRate, discount
        });
        
        const invoiceData = {
            business_name: businessName,
            business_address: businessAddress,
            business_phone: businessPhone,
            business_email: businessEmail,
            client_name: clientName,
            client_address: clientAddress,
            client_phone: clientPhone,
            client_email: clientEmail,
            invoice_number: invoiceNumber,
            invoice_date: invoiceDate,
            tax_rate: taxRate,
            discount: discount,
            payment_terms: paymentTerms,
            items: items
        };
        
        console.log('✅ Invoice data prepared successfully');
        console.log('🌐 Making API request to /api/create-invoice...');
        
        const response = await InvoiceGenerator.apiRequest('/api/create-invoice', {
            method: 'POST',
            body: JSON.stringify(invoiceData)
        });
        
        console.log('✅ API response received:', response);
        
        currentInvoiceData = {
            ...invoiceData,
            ...response
        };
          console.log('🎯 Hiding loading modal...');
        InvoiceGenerator.hideLoadingModal();
        resetSubmitButton(); // Reset the button state
        
        console.log('🎉 Showing success modal...');
        showSuccessModal(response);
        
        // Clear saved data
        localStorage.removeItem('invoice_draft');
        localStorage.removeItem('invoice_items');
        
        console.log('✅ Invoice generation completed successfully!');
          } catch (error) {
        console.error('❌ Error generating invoice:', error);
        console.error('❌ Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        
        InvoiceGenerator.hideLoadingModal();
        resetSubmitButton(); // Reset the button state
        InvoiceGenerator.showToast(`Error generating invoice: ${error.message}`, 'danger');
        
        // Show detailed error in console
        console.log('🔍 Debugging information:');
        console.log('- Items array:', items);
        console.log('- Form element:', document.getElementById('invoiceForm'));
        console.log('- Business name field:', document.getElementById('businessName'));
        console.log('- Client name field:', document.getElementById('clientName'));
    }
}

function showSuccessModal(response) {
    const modal = document.getElementById('successModal');
    const summaryDiv = document.getElementById('invoiceSummary');
    
    // Update action buttons
    document.getElementById('downloadPdfBtn').onclick = () => downloadPdf(currentInvoiceData.invoice_number);
    document.getElementById('downloadCsvBtn').onclick = () => downloadCsv(currentInvoiceData.invoice_number);
    document.getElementById('sendEmailBtn').onclick = () => showEmailModal();
    
    // Show invoice summary
    summaryDiv.innerHTML = `
        <div class="invoice-summary">
            <h6>Invoice Summary</h6>
            <div class="row">
                <div class="col-6">Invoice Number:</div>
                <div class="col-6 text-end"><strong>${currentInvoiceData.invoice_number}</strong></div>
            </div>
            <div class="row">
                <div class="col-6">Client:</div>
                <div class="col-6 text-end">${currentInvoiceData.client_name}</div>
            </div>
            <div class="row">
                <div class="col-6">Items:</div>
                <div class="col-6 text-end">${items.length}</div>
            </div>
            <div class="row">
                <div class="col-6">Subtotal:</div>
                <div class="col-6 text-end">${InvoiceGenerator.formatCurrency(response.totals.subtotal)}</div>
            </div>
            ${response.totals.discount_amount > 0 ? `
            <div class="row">
                <div class="col-6">Discount:</div>
                <div class="col-6 text-end text-danger">-${InvoiceGenerator.formatCurrency(response.totals.discount_amount)}</div>
            </div>
            ` : ''}
            ${response.totals.tax_amount > 0 ? `
            <div class="row">
                <div class="col-6">Tax:</div>
                <div class="col-6 text-end">${InvoiceGenerator.formatCurrency(response.totals.tax_amount)}</div>
            </div>
            ` : ''}
            <div class="row">
                <div class="col-6"><strong>Total:</strong></div>
                <div class="col-6 text-end"><strong>${InvoiceGenerator.formatCurrency(response.totals.total)}</strong></div>
            </div>
        </div>
    `;
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

function downloadPdf(invoiceNumber) {
    window.open(`/api/download-pdf/${invoiceNumber}`, '_blank');
}

function downloadCsv(invoiceNumber) {
    window.open(`/api/export-csv/${invoiceNumber}`, '_blank');
}

function previewInvoice() {
    if (items.length === 0) {
        InvoiceGenerator.showToast('Please add items to preview the invoice', 'warning');
        return;
    }
    
    const totals = calculateTotals();
    const businessName = document.getElementById('businessName').value || 'Your Business';
    const clientName = document.getElementById('clientName').value || 'Client Name';
    const invoiceNumber = document.getElementById('invoiceNumber').value || 'INV-001';
    
    const previewWindow = window.open('', '_blank', 'width=800,height=600');
    previewWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Invoice Preview - ${invoiceNumber}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .business-info, .client-info { margin-bottom: 20px; }
                .invoice-details { margin-bottom: 30px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .totals { text-align: right; }
                .total-row { font-weight: bold; background-color: #f8f9fa; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>INVOICE PREVIEW</h1>
                <h2>${invoiceNumber}</h2>
            </div>
            
            <div class="business-info">
                <h3>From:</h3>
                <p><strong>${businessName}</strong></p>
            </div>
            
            <div class="client-info">
                <h3>To:</h3>
                <p><strong>${clientName}</strong></p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${items.map(item => `
                        <tr>
                            <td>${item.description}</td>
                            <td>${item.quantity}</td>
                            <td>$${item.unit_price.toFixed(2)}</td>
                            <td>$${item.total_price.toFixed(2)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            
            <div class="totals">
                <p>Subtotal: $${totals.subtotal.toFixed(2)}</p>
                ${totals.discountAmount > 0 ? `<p>Discount: -$${totals.discountAmount.toFixed(2)}</p>` : ''}
                ${totals.taxAmount > 0 ? `<p>Tax: $${totals.taxAmount.toFixed(2)}</p>` : ''}
                <p class="total-row">TOTAL: $${totals.grandTotal.toFixed(2)}</p>
            </div>
        </body>
        </html>
    `);
    previewWindow.document.close();
}

function clearForm() {
    if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
        document.getElementById('invoiceForm').reset();
        items = [];
        document.getElementById('itemsTableBody').innerHTML = '';
        calculateTotals();
        
        // Reset date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('invoiceDate').value = today;
        
        // Generate new invoice number
        generateInvoiceNumber();
        
        // Clear localStorage
        localStorage.removeItem('invoice_draft');
        localStorage.removeItem('invoice_items');
        
        InvoiceGenerator.showToast('Form cleared successfully', 'info');
    }
}

function runDiagnostic() {
    console.clear();
    console.log('🔍 INVOICE GENERATOR DIAGNOSTIC');
    console.log('==============================');
    
    // Check all required form elements
    const requiredElements = [
        'businessName', 'businessAddress', 'businessPhone', 'businessEmail',
        'clientName', 'clientAddress', 'clientPhone', 'clientEmail',
        'invoiceNumber', 'invoiceDate', 'taxRate', 'discount', 'paymentTerms'
    ];

    let missingElements = [];
    let emptyRequired = [];

    requiredElements.forEach(elementId => {
        const element = document.getElementById(elementId);
        if (element) {
            console.log(`✅ ${elementId}: Found (value: "${element.value}")`);
            if (element.required && (!element.value || !element.value.trim())) {
                emptyRequired.push(elementId);
            }
        } else {
            console.log(`❌ ${elementId}: NOT FOUND`);
            missingElements.push(elementId);
        }
    });

    // Check InvoiceGenerator object
    console.log('\n🔧 InvoiceGenerator Functions:');
    if (window.InvoiceGenerator) {
        console.log('✅ InvoiceGenerator object found');
        const methods = ['showToast', 'formatCurrency', 'showLoadingModal', 'hideLoadingModal', 'apiRequest', 'validateRequired'];
        methods.forEach(method => {
            if (typeof InvoiceGenerator[method] === 'function') {
                console.log(`✅ ${method}: Available`);
            } else {
                console.log(`❌ ${method}: NOT Available`);
            }
        });
    } else {
        console.log('❌ InvoiceGenerator object not found!');
    }

    // Check items array
    console.log('\n📋 Items Array:');
    if (typeof items !== 'undefined') {
        console.log(`✅ Items array exists with ${items.length} items`);
        if (items.length > 0) {
            items.forEach((item, index) => {
                console.log(`   ${index + 1}. ${item.description} - Qty: ${item.quantity} - Price: $${item.unit_price}`);
            });
        } else {
            console.log('⚠️ No items added yet');
        }
    } else {
        console.log('❌ Items array not found!');
    }

    // Test form validation
    console.log('\n🧪 Form Validation Test:');
    const form = document.getElementById('invoiceForm');
    if (form && window.InvoiceGenerator) {
        const isValid = InvoiceGenerator.validateRequired(form);
        console.log(`Form validation result: ${isValid ? '✅ VALID' : '❌ INVALID'}`);
        
        if (emptyRequired.length > 0) {
            console.log(`❌ Empty required fields: ${emptyRequired.join(', ')}`);
        }
    }

    // Test API connectivity
    console.log('\n🌐 Testing API Connectivity:');
    fetch('/api/get-all-invoices')
        .then(response => response.json())
        .then(data => {
            console.log('✅ API connection successful');
            console.log(`📊 Found ${data.invoices ? data.invoices.length : 0} existing invoices`);
        })
        .catch(error => {
            console.log('❌ API connection failed:', error.message);
        });

    // Summary
    console.log('\n📊 DIAGNOSTIC SUMMARY:');
    console.log(`Form elements: ${missingElements.length > 0 ? '❌ Some missing' : '✅ All found'}`);
    console.log(`InvoiceGenerator: ${window.InvoiceGenerator ? '✅ Available' : '❌ Missing'}`);
    console.log(`Items: ${items && items.length > 0 ? '✅ ' + items.length + ' items' : '⚠️ No items'}`);
    console.log(`Required fields: ${emptyRequired.length > 0 ? '❌ ' + emptyRequired.length + ' empty' : '✅ All filled'}`);
    
    // Show result in UI
    if (missingElements.length > 0 || emptyRequired.length > 0 || !window.InvoiceGenerator) {
        InvoiceGenerator?.showToast('Diagnostic found issues - check console (F12)', 'warning');
    } else {
        InvoiceGenerator?.showToast('Diagnostic completed - check console (F12) for details', 'info');
    }
}

function resetSubmitButton() {
    const submitButton = document.querySelector('#invoiceForm button[type="submit"]');
    if (submitButton) {
        submitButton.innerHTML = '<i class="fas fa-file-pdf me-2"></i>Generate Invoice';
        submitButton.disabled = false;
        console.log('✅ Submit button reset');
    }
}

function showEmailModal() {
    console.log('📧 Showing email modal...');
    
    // Load business email configuration
    loadBusinessEmailConfig();
    
    // Pre-populate client email if available
    const clientEmail = document.getElementById('clientEmail').value;
    if (clientEmail) {
        document.getElementById('recipientEmail').value = clientEmail;
    }
    
    // Pre-populate email subject and message with business template
    populateEmailTemplate();
    
    // Show modal
    const emailModal = new bootstrap.Modal(document.getElementById('emailModal'));
    emailModal.show();
}

async function loadBusinessEmailConfig() {
    try {        console.log('📧 Loading business email configuration...');
          // Auto-fill business email credentials
        document.getElementById('senderEmail').value = 'marketerrobi@gmail.com';
        document.getElementById('senderPassword').value = 'moogtnzzgqgzfbpr';
        
        // Hide sender fields since they're pre-configured
        const senderEmailGroup = document.getElementById('senderEmail').closest('.mb-3');
        const senderPasswordGroup = document.getElementById('senderPassword').closest('.mb-3');
        
        if (senderEmailGroup) {
            senderEmailGroup.style.display = 'none';
        }
        if (senderPasswordGroup) {
            senderPasswordGroup.style.display = 'none';
        }
        
        // Add info message about business email
        const emailForm = document.getElementById('emailForm');
        let infoDiv = document.getElementById('businessEmailInfo');
        
        if (!infoDiv) {
            infoDiv = document.createElement('div');
            infoDiv.id = 'businessEmailInfo';
            infoDiv.className = 'alert alert-info';
            infoDiv.innerHTML = `
                <i class="fas fa-info-circle me-2"></i>
                <strong>Business Email:</strong> Emails will be sent from marketerrobi@gmail.com
            `;
            emailForm.insertBefore(infoDiv, emailForm.firstChild);
        }
        
        console.log('✅ Business email configuration loaded');
        
    } catch (error) {
        console.error('❌ Error loading business email config:', error);
        // Fallback to manual entry if config fails
        InvoiceGenerator.showToast('Using manual email entry', 'info');
    }
}

function populateEmailTemplate() {
    const businessName = document.getElementById('businessName').value || 'Marketer Robi';
    const clientName = document.getElementById('clientName').value || 'Valued Client'; 
    const invoiceNumber = currentInvoiceData?.invoice_number || document.getElementById('invoiceNumber').value;
    const invoiceDate = document.getElementById('invoiceDate').value;
    const paymentTerms = document.getElementById('paymentTerms').value || 'Net 30 days';
    
    // Calculate total amount
    const totals = calculateTotals();
    const totalAmount = totals.grandTotal.toFixed(2);
    
    // Set professional subject
    const subject = `Invoice from Marketer Robi - #${invoiceNumber}`;
    document.getElementById('emailSubject').value = subject;
    
    // Set professional message template
    const message = `Dear ${clientName},

Please find attached your invoice #${invoiceNumber} dated ${invoiceDate}.

Invoice Details:
- Invoice Number: ${invoiceNumber}
- Total Amount: $${totalAmount}
- Payment Terms: ${paymentTerms}

Thank you for your business!

Best regards,
Marketer Robi
marketerrobi@gmail.com`;
    
    document.getElementById('emailMessage').value = message;
}

async function sendInvoiceEmail() {
    console.log('📤 Starting email send process...');
    
    // Validate email form
    const senderEmail = document.getElementById('senderEmail').value.trim();
    const senderPassword = document.getElementById('senderPassword').value.trim();
    const recipientEmail = document.getElementById('recipientEmail').value.trim();
    
    if (!senderEmail || !senderPassword || !recipientEmail) {
        InvoiceGenerator.showToast('Please fill in all required email fields', 'danger');
        return;
    }
    
    // Validate email addresses
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(senderEmail)) {
        InvoiceGenerator.showToast('Please enter a valid sender email address', 'danger');
        return;
    }
    
    if (!emailRegex.test(recipientEmail)) {
        InvoiceGenerator.showToast('Please enter a valid recipient email address', 'danger');
        return;
    }
    
    if (!currentInvoiceData?.invoice_number) {
        InvoiceGenerator.showToast('No invoice data available. Please generate invoice first.', 'danger');
        return;
    }
    
    // Show loading
    const loadingModal = InvoiceGenerator.showLoadingModal('Sending Email...', 'Sending your invoice via email. This may take a moment.');
    
    try {
        const emailData = {
            invoice_number: currentInvoiceData.invoice_number,
            sender_email: senderEmail,
            sender_password: senderPassword,
            recipient_email: recipientEmail,
            email_subject: document.getElementById('emailSubject').value.trim() || `Invoice ${currentInvoiceData.invoice_number}`,
            email_message: document.getElementById('emailMessage').value.trim()
        };
        
        console.log('📧 Sending email with data:', {
            ...emailData,
            sender_password: '[HIDDEN]' // Don't log password
        });
        
        const response = await InvoiceGenerator.apiRequest('/api/send-email', {
            method: 'POST',
            body: JSON.stringify(emailData)
        });
        
        console.log('✅ Email sent successfully:', response);
        
        // Hide loading modal
        InvoiceGenerator.hideLoadingModal();
        
        // Hide email modal
        const emailModal = bootstrap.Modal.getInstance(document.getElementById('emailModal'));
        if (emailModal) {
            emailModal.hide();
        }
        
        // Show success message
        InvoiceGenerator.showToast('📧 Invoice sent successfully via email!', 'success');
        
        // Clear sensitive data
        document.getElementById('senderPassword').value = '';
        
    } catch (error) {
        console.error('❌ Error sending email:', error);
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast(`Error sending email: ${error.message}`, 'danger');
    }
}

function toggleSenderFields() {
    const senderEmailGroup = document.getElementById('senderEmailGroup');
    const senderPasswordGroup = document.getElementById('senderPasswordGroup');
    const toggleBtn = event.target.closest('button');
    
    if (senderEmailGroup.style.display === 'none') {
        // Show advanced settings
        senderEmailGroup.style.display = 'block';
        senderPasswordGroup.style.display = 'block';
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash me-1"></i>Hide Advanced Settings';
        toggleBtn.className = 'btn btn-outline-warning btn-sm';
    } else {
        // Hide advanced settings
        senderEmailGroup.style.display = 'none';
        senderPasswordGroup.style.display = 'none';        toggleBtn.innerHTML = '<i class="fas fa-cog me-1"></i>Advanced Email Settings';
        toggleBtn.className = 'btn btn-outline-info btn-sm';
          // Reset to business email
        document.getElementById('senderEmail').value = 'marketerrobi@gmail.com';
        document.getElementById('senderPassword').value = 'moogtnzzgqgzfbpr';
    }
}

async function testEmailConnection() {
    console.log('🧪 Testing email connection...');
    
    const senderEmail = document.getElementById('senderEmail').value || 'marketerrobi@gmail.com';
    const senderPassword = document.getElementById('senderPassword').value || 'NotFound#404';
    
    if (!senderEmail || !senderPassword) {
        InvoiceGenerator.showToast('Email credentials are required for testing', 'warning');
        return;
    }
    
    const loadingModal = InvoiceGenerator.showLoadingModal('Testing Email Connection...', 'Checking Gmail authentication and connection.');
    
    try {
        const testData = {
            sender_email: senderEmail,
            sender_password: senderPassword
        };
        
        console.log('🔧 Testing email connection with:', senderEmail);
        
        const response = await InvoiceGenerator.apiRequest('/api/test-email', {
            method: 'POST',
            body: JSON.stringify(testData)
        });
        
        console.log('📧 Email test response:', response);
        
        InvoiceGenerator.hideLoadingModal();
        
        if (response.success) {
            InvoiceGenerator.showToast('✅ Email connection successful! Ready to send invoices.', 'success');
        } else {
            InvoiceGenerator.showToast(`❌ Email connection failed: ${response.message}`, 'danger');
            
            // Show troubleshooting tips
            setTimeout(() => {
                alert(`📧 Gmail Setup Help:

1. Enable 2-Factor Authentication in your Google Account
2. Go to Google Account > Security > App passwords
3. Generate a new App Password for "Mail"
4. Use that App Password (not your regular password)
5. Make sure you're using: marketerrobi@gmail.com

Current error: ${response.message}`);
            }, 2000);
        }
        
    } catch (error) {
        console.error('❌ Email test error:', error);
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast(`Email test failed: ${error.message}`, 'danger');
    }
}
