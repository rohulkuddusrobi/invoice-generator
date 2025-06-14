// View Invoices JavaScript

let allInvoices = [];
let filteredInvoices = [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    loadInvoices();
    setupEventListeners();
});

function setupEventListeners() {
    // Search filter
    document.getElementById('searchFilter').addEventListener('input', debounce(applyFilters, 300));
    
    // Date filters
    document.getElementById('dateFromFilter').addEventListener('change', applyFilters);
    document.getElementById('dateToFilter').addEventListener('change', applyFilters);
}

async function loadInvoices() {
    try {
        const response = await InvoiceGenerator.apiRequest('/api/get-all-invoices');
        allInvoices = response.invoices || [];
        filteredInvoices = [...allInvoices];
        
        updateInvoicesTable();
        updateInvoiceCount();
        
    } catch (error) {
        InvoiceGenerator.showToast(`Error loading invoices: ${error.message}`, 'danger');
    }
}

function updateInvoicesTable() {
    const tbody = document.getElementById('invoicesTableBody');
    
    if (filteredInvoices.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <i class="fas fa-file-invoice fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No invoices found</h5>
                    <p class="text-muted">Try adjusting your filters or create a new invoice.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filteredInvoices.map(invoice => `
        <tr data-invoice="${invoice.number}">
            <td>
                <strong class="text-primary">${invoice.number}</strong>
            </td>
            <td>${InvoiceGenerator.formatDate(invoice.date)}</td>
            <td>${invoice.client}</td>
            <td>
                <span class="badge bg-info">${invoice.items_count} items</span>
            </td>
            <td>
                <strong class="text-success">${InvoiceGenerator.formatCurrency(invoice.total)}</strong>
            </td>
            <td>
                <div class="btn-group btn-group-sm" role="group">
                    <button type="button" class="btn btn-outline-primary" onclick="viewInvoice('${invoice.number}')" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button type="button" class="btn btn-outline-success" onclick="downloadPdf('${invoice.number}')" title="Download PDF">
                        <i class="fas fa-file-pdf"></i>
                    </button>
                    <button type="button" class="btn btn-outline-info" onclick="exportCsv('${invoice.number}')" title="Export CSV">
                        <i class="fas fa-file-csv"></i>
                    </button>
                    <button type="button" class="btn btn-outline-warning" onclick="sendEmail('${invoice.number}')" title="Send Email">
                        <i class="fas fa-envelope"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function updateInvoiceCount() {
    document.getElementById('invoiceCount').textContent = filteredInvoices.length;
}

function applyFilters() {
    const searchTerm = document.getElementById('searchFilter').value.toLowerCase();
    const dateFrom = document.getElementById('dateFromFilter').value;
    const dateTo = document.getElementById('dateToFilter').value;
    
    filteredInvoices = allInvoices.filter(invoice => {
        // Search filter
        const matchesSearch = !searchTerm || 
            invoice.number.toLowerCase().includes(searchTerm) ||
            invoice.client.toLowerCase().includes(searchTerm);
        
        // Date filters
        const invoiceDate = new Date(invoice.date);
        const matchesDateFrom = !dateFrom || invoiceDate >= new Date(dateFrom);
        const matchesDateTo = !dateTo || invoiceDate <= new Date(dateTo);
        
        return matchesSearch && matchesDateFrom && matchesDateTo;
    });
    
    updateInvoicesTable();
    updateInvoiceCount();
}

async function viewInvoice(invoiceNumber) {
    console.log('🔍 Viewing invoice:', invoiceNumber);
    
    let loadingModal = null;
    
    try {
        // Show loading state on the button
        const viewBtn = document.querySelector(`button[onclick="viewInvoice('${invoiceNumber}')"]`);
        let originalBtnContent = '';
        
        if (viewBtn) {
            originalBtnContent = viewBtn.innerHTML;
            viewBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            viewBtn.disabled = true;
        }
        
        // Show loading modal
        loadingModal = InvoiceGenerator.showLoadingModal('Loading Invoice...', 'Fetching invoice details...');
        
        // Add a small delay to ensure modal is visible
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Fetch invoice data
        console.log('📡 Fetching invoice data for:', invoiceNumber);
        const response = await InvoiceGenerator.apiRequest(`/api/get-invoice/${invoiceNumber}`);
        
        console.log('✅ Invoice data received:', response);
        
        // Hide loading modal
        InvoiceGenerator.hideLoadingModal();
        
        // Restore button state
        if (viewBtn) {
            viewBtn.innerHTML = originalBtnContent;
            viewBtn.disabled = false;
        }
        
        // Check if we have valid data
        if (response && response.success && response.data) {
            // Show invoice modal
            showInvoiceModal(response.data);
        } else {
            throw new Error('Invalid response data received');
        }
        
    } catch (error) {
        console.error('❌ Error loading invoice:', error);
        
        // Hide loading modal
        if (loadingModal) {
            InvoiceGenerator.hideLoadingModal();
        }
        
        // Restore button state
        const viewBtn = document.querySelector(`button[onclick="viewInvoice('${invoiceNumber}')"]`);
        if (viewBtn) {
            viewBtn.innerHTML = '<i class="fas fa-eye"></i>';
            viewBtn.disabled = false;
        }
        
        // Show error message
        const errorMessage = error.message || 'Failed to load invoice details';
        InvoiceGenerator.showToast(`Error loading invoice: ${errorMessage}`, 'danger');
    }
}

function showInvoiceModal(invoiceData) {
    console.log('📋 Showing invoice modal for:', invoiceData);
    
    try {
        const modal = document.getElementById('invoiceModal');
        const modalBody = document.getElementById('invoiceModalBody');
        
        if (!modal || !modalBody) {
            throw new Error('Invoice modal elements not found');
        }
        
        // Validate required data
        if (!invoiceData || !invoiceData.invoice_number) {
            throw new Error('Invalid invoice data');
        }
        
        // Set default values for missing data
        const businessInfo = invoiceData.business_info || {};
        const clientInfo = invoiceData.client_info || {};
        const totals = invoiceData.totals || {};
        const items = invoiceData.items || [];
        
        // Update modal content
        modalBody.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-6">
                    <h6 class="text-primary mb-3">
                        <i class="fas fa-building me-2"></i>Business Information
                    </h6>
                    <div class="card">
                        <div class="card-body">
                            <p class="mb-2"><strong>${businessInfo.name || 'N/A'}</strong></p>
                            <p class="mb-2 text-muted">${businessInfo.address || 'N/A'}</p>
                            <p class="mb-2"><i class="fas fa-phone me-2"></i>${businessInfo.phone || 'N/A'}</p>
                            ${businessInfo.email ? `<p class="mb-0"><i class="fas fa-envelope me-2"></i>${businessInfo.email}</p>` : ''}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6 class="text-success mb-3">
                        <i class="fas fa-user me-2"></i>Client Information
                    </h6>
                    <div class="card">
                        <div class="card-body">
                            <p class="mb-2"><strong>${clientInfo.name || 'N/A'}</strong></p>
                            <p class="mb-2 text-muted">${clientInfo.address || 'N/A'}</p>
                            <p class="mb-2"><i class="fas fa-phone me-2"></i>${clientInfo.phone || 'N/A'}</p>
                            ${clientInfo.email ? `<p class="mb-0"><i class="fas fa-envelope me-2"></i>${clientInfo.email}</p>` : ''}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    <h6 class="text-info mb-3">
                        <i class="fas fa-file-invoice me-2"></i>Invoice Details
                    </h6>
                    <div class="card">
                        <div class="card-body">
                            <p class="mb-2"><strong>Invoice #:</strong> ${invoiceData.invoice_number}</p>
                            <p class="mb-2"><strong>Date:</strong> ${InvoiceGenerator.formatDate(invoiceData.invoice_date)}</p>
                            <p class="mb-2"><strong>Tax Rate:</strong> ${invoiceData.tax_rate || 0}%</p>
                            <p class="mb-2"><strong>Discount:</strong> ${invoiceData.discount || 0}%</p>
                            ${invoiceData.payment_terms ? `<p class="mb-0"><strong>Payment Terms:</strong> ${invoiceData.payment_terms}</p>` : ''}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6 class="text-warning mb-3">
                        <i class="fas fa-calculator me-2"></i>Summary
                    </h6>
                    <div class="card">
                        <div class="card-body">
                            <p class="mb-2"><strong>Items:</strong> ${items.length}</p>
                            <p class="mb-2"><strong>Subtotal:</strong> ${InvoiceGenerator.formatCurrency(totals.subtotal || 0)}</p>
                            ${totals.discount_amount > 0 ? `<p class="mb-2"><strong>Discount:</strong> -${InvoiceGenerator.formatCurrency(totals.discount_amount)}</p>` : ''}
                            ${totals.tax_amount > 0 ? `<p class="mb-2"><strong>Tax:</strong> ${InvoiceGenerator.formatCurrency(totals.tax_amount)}</p>` : ''}
                            <p class="mb-0"><strong class="text-success fs-5">Total: ${InvoiceGenerator.formatCurrency(totals.total || 0)}</strong></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mb-4">
                <h6 class="text-dark mb-3">
                    <i class="fas fa-list me-2"></i>Items
                </h6>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Description</th>
                                <th>Quantity</th>
                                <th>Unit Price</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${items.length > 0 ? items.map(item => `
                                <tr>
                                    <td>${item.description || 'N/A'}</td>
                                    <td>${item.quantity || 0}</td>
                                    <td>${InvoiceGenerator.formatCurrency(item.unit_price || 0)}</td>
                                    <td>${InvoiceGenerator.formatCurrency(item.total_price || 0)}</td>
                                </tr>
                            `).join('') : `
                                <tr>
                                    <td colspan="4" class="text-center text-muted">No items found</td>
                                </tr>
                            `}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        // Update download button
        const downloadBtn = document.getElementById('modalDownloadPdf');
        if (downloadBtn) {
            downloadBtn.onclick = () => downloadPdf(invoiceData.invoice_number);
        }
        
        // Show modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
      } catch (error) {
        console.error('❌ Error showing invoice modal:', error);
        InvoiceGenerator.showToast(`Error displaying invoice: ${error.message}`, 'danger');
    }
}

function downloadPdf(invoiceNumber) {
    console.log('📥 Downloading PDF for invoice:', invoiceNumber);
    
    try {
        // Show loading state on the button
        const downloadBtn = document.querySelector(`button[onclick="downloadPdf('${invoiceNumber}')"]`);
        if (downloadBtn) {
            const originalContent = downloadBtn.innerHTML;
            downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            downloadBtn.disabled = true;
            
            // Restore button after download
            setTimeout(() => {
                downloadBtn.innerHTML = originalContent;
                downloadBtn.disabled = false;
            }, 2000);
        }
        
        // Show brief loading modal
        const loadingModal = InvoiceGenerator.showLoadingModal('Preparing Download...', 'Generating PDF file...');
        
        // Create download link
        const link = document.createElement('a');
        link.href = `/api/download-pdf/${invoiceNumber}`;
        link.download = `invoice_${invoiceNumber}.pdf`;
        
        // Add to DOM, click, and remove
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Hide loading modal after download starts
        setTimeout(() => {
            InvoiceGenerator.hideLoadingModal();
            InvoiceGenerator.showToast('Download started!', 'success');
        }, 1000);
        
    } catch (error) {
        console.error('❌ Error downloading PDF:', error);
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast(`Error downloading PDF: ${error.message}`, 'danger');
          // Restore button state
        const downloadBtn = document.querySelector(`button[onclick="downloadPdf('${invoiceNumber}')"]`);
        if (downloadBtn) {
            downloadBtn.innerHTML = '<i class="fas fa-file-pdf"></i>';
            downloadBtn.disabled = false;
        }
    }
}

function exportCsv(invoiceNumber) {
    console.log('📊 Exporting CSV for invoice:', invoiceNumber);
    
    try {
        // Show loading state on the button
        const exportBtn = document.querySelector(`button[onclick="exportCsv('${invoiceNumber}')"]`);
        if (exportBtn) {
            const originalContent = exportBtn.innerHTML;
            exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            exportBtn.disabled = true;
            
            // Restore button after export
            setTimeout(() => {
                exportBtn.innerHTML = originalContent;
                exportBtn.disabled = false;
            }, 2000);
        }
        
        // Show brief loading modal
        const loadingModal = InvoiceGenerator.showLoadingModal('Exporting CSV...', 'Preparing CSV file...');
        
        // Create download link
        const link = document.createElement('a');
        link.href = `/api/export-csv/${invoiceNumber}`;
        link.download = `invoice_${invoiceNumber}.csv`;
        
        // Add to DOM, click, and remove
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Hide loading modal after export starts
        setTimeout(() => {
            InvoiceGenerator.hideLoadingModal();
            InvoiceGenerator.showToast('CSV export started!', 'success');
        }, 1000);
        
    } catch (error) {
        console.error('❌ Error exporting CSV:', error);
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast(`Error exporting CSV: ${error.message}`, 'danger');
        
        // Restore button state
        const exportBtn = document.querySelector(`button[onclick="exportCsv('${invoiceNumber}')"]`);
        if (exportBtn) {
            exportBtn.innerHTML = '<i class="fas fa-file-csv"></i>';
            exportBtn.disabled = false;
        }
    }
}

function sendEmail(invoiceNumber) {
    console.log('📧 Opening email modal for invoice:', invoiceNumber);
    
    // Set invoice number in the modal
    document.getElementById('emailInvoiceNumber').textContent = invoiceNumber;
      // Auto-fill business email credentials
    document.getElementById('senderEmail').value = 'marketerrobi@gmail.com';
    document.getElementById('senderPassword').value = 'moogtnzzgqgzfbpr';
    
    // Hide sender fields since they're pre-configured
    const senderEmailGroup = document.getElementById('senderEmail').closest('.mb-3');
    const senderPasswordGroup = document.getElementById('senderPassword').closest('.mb-3');
    
    if (senderEmailGroup) senderEmailGroup.style.display = 'none';
    if (senderPasswordGroup) senderPasswordGroup.style.display = 'none';
    
    // Try to pre-fill data from invoice
    const invoice = allInvoices.find(inv => inv.number === invoiceNumber);
    if (invoice) {
        // Pre-fill professional subject
        document.getElementById('emailSubject').value = `Invoice from Marketer Robi - #${invoiceNumber}`;
        
        // Pre-fill professional message
        const message = `Dear ${invoice.client},

Please find attached your invoice #${invoiceNumber} dated ${invoice.date}.

Invoice Details:
- Invoice Number: ${invoiceNumber}
- Total Amount: $${invoice.total.toFixed(2)}
- Items: ${invoice.items_count} items

Thank you for your business!

Best regards,
Marketer Robi
marketerrobi@gmail.com`;
        
        document.getElementById('emailMessage').value = message;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('emailModal'));
    modal.show();
}

async function sendInvoiceEmail() {
    console.log('📤 Starting invoice email send...');
    
    const invoiceNumber = document.getElementById('emailInvoiceNumber').textContent;
    const senderEmail = document.getElementById('senderEmail').value.trim();
    const senderPassword = document.getElementById('senderPassword').value.trim();
    const recipientEmail = document.getElementById('recipientEmail').value.trim();
    const emailSubject = document.getElementById('emailSubject').value.trim();
    const emailMessage = document.getElementById('emailMessage').value.trim();
    
    // Validation
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
    
    const loadingModal = InvoiceGenerator.showLoadingModal('Sending Email...', 'Sending invoice via email. This may take a moment.');
    
    try {
        const emailData = {
            invoice_number: invoiceNumber,
            sender_email: senderEmail,
            sender_password: senderPassword,
            recipient_email: recipientEmail,
            email_subject: emailSubject || `Invoice ${invoiceNumber}`,
            email_message: emailMessage
        };
        
        console.log('📧 Sending email with data:', {
            ...emailData,
            sender_password: '[HIDDEN]'
        });
        
        const response = await InvoiceGenerator.apiRequest('/api/send-email', {
            method: 'POST',
            body: JSON.stringify(emailData)
        });
        
        console.log('✅ Email sent successfully:', response);
        
        InvoiceGenerator.hideLoadingModal();
        
        // Hide email modal
        const emailModal = bootstrap.Modal.getInstance(document.getElementById('emailModal'));
        if (emailModal) {
            emailModal.hide();
        }
        
        InvoiceGenerator.showToast('📧 Invoice sent successfully via email!', 'success');
        
        // Clear sensitive data
        document.getElementById('senderPassword').value = '';
        
    } catch (error) {
        console.error('❌ Error sending email:', error);
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast(`Error sending email: ${error.message}`, 'danger');
    }
}

function exportAllInvoices() {
    if (allInvoices.length === 0) {
        InvoiceGenerator.showToast('No invoices to export', 'warning');
        return;
    }
    
    const loadingModal = InvoiceGenerator.showLoadingModal('Exporting All Invoices...', 'Preparing summary CSV file.');
    
    // Create CSV content
    const headers = ['Invoice Number', 'Date', 'Client', 'Items', 'Total'];
    const csvContent = [
        headers.join(','),
        ...allInvoices.map(invoice => [
            invoice.number,
            invoice.date,
            `"${invoice.client}"`,
            invoice.items_count,
            invoice.total
        ].join(','))
    ].join('\n');
    
    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `all_invoices_${new Date().toISOString().split('T')[0]}.csv`;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    window.URL.revokeObjectURL(url);
    
    setTimeout(() => {
        InvoiceGenerator.hideLoadingModal();
        InvoiceGenerator.showToast('Export completed successfully');
    }, 1000);
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
