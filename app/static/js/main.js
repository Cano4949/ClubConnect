// ClubConnect Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validations
    initializeFormValidation();
    
    // Initialize delete confirmations
    initializeDeleteConfirmations();
    
    // Initialize date/time pickers
    initializeDateTimePickers();
    
    // Initialize search functionality
    initializeSearch();
    
    // Auto-dismiss alerts
    autoDismissAlerts();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation
function initializeFormValidation() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Delete confirmations
function initializeDeleteConfirmations() {
    document.querySelectorAll('.delete-confirm').forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const itemName = this.getAttribute('data-item-name') || 'dieses Element';
            const deleteUrl = this.getAttribute('href') || this.getAttribute('data-url');
            
            if (confirm(`Möchten Sie ${itemName} wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.`)) {
                if (this.tagName === 'A') {
                    window.location.href = deleteUrl;
                } else {
                    // For forms
                    const form = this.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }
        });
    });
}

// Initialize date and time pickers
function initializeDateTimePickers() {
    // Add date picker to date inputs
    document.querySelectorAll('input[type="date"]').forEach(function(input) {
        // Set min date to today for future events
        if (input.classList.contains('future-date')) {
            const today = new Date().toISOString().split('T')[0];
            input.setAttribute('min', today);
        }
    });
    
    // Format time inputs
    document.querySelectorAll('input[type="time"]').forEach(function(input) {
        input.setAttribute('step', '300'); // 5-minute intervals
    });
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.table-search');
    
    searchInputs.forEach(function(searchInput) {
        const targetTable = document.querySelector(searchInput.getAttribute('data-table'));
        
        if (targetTable) {
            searchInput.addEventListener('keyup', function() {
                const searchTerm = this.value.toLowerCase();
                const rows = targetTable.querySelectorAll('tbody tr');
                
                rows.forEach(function(row) {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            });
        }
    });
}

// Auto-dismiss alerts after 5 seconds
function autoDismissAlerts() {
    document.querySelectorAll('.alert.alert-dismissible').forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// Player filter functionality
function filterPlayers(team) {
    const url = new URL(window.location);
    if (team === 'all') {
        url.searchParams.delete('team');
    } else {
        url.searchParams.set('team', team);
    }
    window.location = url;
}

// Event filter functionality
function filterEvents(type) {
    const url = new URL(window.location);
    if (type === 'all') {
        url.searchParams.delete('type');
    } else {
        url.searchParams.set('type', type);
    }
    window.location = url;
}

// Bulk invite functionality
function toggleAllInvites(checkbox) {
    const checkboxes = document.querySelectorAll('.invite-checkbox');
    checkboxes.forEach(function(cb) {
        cb.checked = checkbox.checked;
    });
}

// Update invite status
function updateInviteStatus(inviteId, status) {
    fetch(`/admin/invite/${inviteId}/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Fehler beim Aktualisieren des Status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ein Fehler ist aufgetreten');
    });
}

// Get CSRF token
function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Print functionality
function printPage() {
    window.print();
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        
        cols.forEach(function(col) {
            // Remove any buttons or actions column
            if (!col.classList.contains('no-export')) {
                rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
            }
        });
        
        csv.push(rowData.join(','));
    });
    
    // Download CSV
    const csvContent = 'data:text/csv;charset=utf-8,' + csv.join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', filename + '.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Calendar navigation
function navigateCalendar(month, year) {
    const url = new URL(window.location);
    url.searchParams.set('month', month);
    url.searchParams.set('year', year);
    window.location = url;
}

// Toggle password visibility
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const icon = event.target;
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
}

// Character counter for textareas
document.querySelectorAll('textarea[maxlength]').forEach(function(textarea) {
    const maxLength = textarea.getAttribute('maxlength');
    const counter = document.createElement('small');
    counter.className = 'text-muted';
    counter.textContent = `0 / ${maxLength}`;
    textarea.parentNode.appendChild(counter);
    
    textarea.addEventListener('input', function() {
        const currentLength = this.value.length;
        counter.textContent = `${currentLength} / ${maxLength}`;
        
        if (currentLength > maxLength * 0.9) {
            counter.classList.add('text-danger');
        } else {
            counter.classList.remove('text-danger');
        }
    });
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Show scroll to top button when scrolled down
window.addEventListener('scroll', function() {
    const scrollButton = document.getElementById('scrollToTop');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});
