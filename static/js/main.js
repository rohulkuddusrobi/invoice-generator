// Main JavaScript file for Invoice Generator

// Global variables
let currentInvoiceNumber = '';

// Utility functions
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showLoadingModal(title = 'Processing...', subtitle = 'Please wait.') {
    console.log('🎯 showLoadingModal called:', { title, subtitle });
    
    const modal = document.getElementById('loadingModal');
    if (!modal) {
        console.error('❌ Loading modal element not found');
        return null;
    }
    
    const titleElement = document.getElementById('loadingText');
    const subtitleElement = document.getElementById('loadingSubtext');
    
    if (titleElement) {
        titleElement.textContent = title;
    }
    
    if (subtitleElement) {
        subtitleElement.textContent = subtitle;
    }
    
    try {
        // Hide any other modals first
        const existingModals = document.querySelectorAll('.modal.show');
        existingModals.forEach(existingModal => {
            const bsExistingModal = bootstrap.Modal.getInstance(existingModal);
            if (bsExistingModal && existingModal.id !== 'loadingModal') {
                bsExistingModal.hide();
            }
        });
        
        // Show loading modal
        const bsModal = new bootstrap.Modal(modal, {
            backdrop: 'static',
            keyboard: false
        });
        bsModal.show();
        
        console.log('✅ Loading modal shown successfully');
        return bsModal;
    } catch (error) {
        console.error('❌ Error showing modal:', error);
        return null;
    }
}

function hideLoadingModal() {
    console.log('🎯 hideLoadingModal called');
    
    const modal = document.getElementById('loadingModal');
    if (!modal) {
        console.error('❌ Loading modal element not found for hiding');
        return;
    }
    
    try {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
            console.log('✅ Loading modal hidden successfully');
        } else {
            // Force hide if no instance found
            console.warn('⚠️ No Bootstrap modal instance found, forcing hide');
            modal.classList.remove('show');
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
            modal.removeAttribute('aria-modal');
            
            // Remove backdrop
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
            
            // Remove modal-open class from body
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
        }
    } catch (error) {
        console.error('❌ Error hiding modal:', error);
        // Force cleanup on error
        modal.classList.remove('show');
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) backdrop.remove();
    }
}

// API helper functions
async function apiRequest(url, options = {}) {
    console.log('🌐 API Request:', url, options);
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
        
        const response = await fetch(url, {
            signal: controller.signal,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        clearTimeout(timeoutId);
        
        console.log('📡 Response status:', response.status, response.statusText);
        
        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch (e) {
                // If JSON parsing fails, use the default error message
                console.warn('Could not parse error response as JSON');
            }
            
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        console.log('✅ API Response:', data);
        
        return data;
    } catch (error) {
        console.error('❌ API Request Error:', error);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. Please try again.');
        }
        
        if (error.message.includes('Failed to fetch')) {
            throw new Error('Network error. Please check your connection and try again.');
        }
        
        throw error;
    }
}

// Download helper functions
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Form validation
function validateRequired(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value || !field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Number formatting
function parseNumber(value) {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? 0 : parsed;
}

// Local storage helpers
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// Auto-save functionality
function autoSaveForm(formId, key) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Load saved data
    const savedData = loadFromLocalStorage(key);
    if (savedData) {
        Object.keys(savedData).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"], #${fieldName}`);
            if (field) {
                field.value = savedData[fieldName];
            }
        });
    }
    
    // Save on input
    form.addEventListener('input', debounce(() => {
        const formData = new FormData(form);
        const data = {};
        
        // Get all form inputs
        form.querySelectorAll('input, textarea, select').forEach(field => {
            if (field.id || field.name) {
                data[field.id || field.name] = field.value;
            }
        });
        
        saveToLocalStorage(key, data);
    }, 1000));
}

// Debounce function
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

// Initialize common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);    // Add loading states to buttons (except invoice form buttons)
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        // Skip buttons inside the invoice form - they have their own handling
        if (button.closest('#invoiceForm')) {
            return;
        }
        
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                this.disabled = true;
            }
        });
    });
});

// Export functions for use in other files
window.InvoiceGenerator = {
    showToast,
    formatCurrency,
    formatDate,
    showLoadingModal,
    hideLoadingModal,
    apiRequest,
    downloadFile,
    validateRequired,
    parseNumber,
    saveToLocalStorage,
    loadFromLocalStorage,
    autoSaveForm
};
