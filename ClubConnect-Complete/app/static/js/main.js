// ClubConnect Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = button.getAttribute('data-confirm-delete') || 'Sind Sie sicher, dass Sie diesen Eintrag löschen möchten?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Loading states for buttons
    var loadingButtons = document.querySelectorAll('[data-loading-text]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var originalText = button.innerHTML;
            var loadingText = button.getAttribute('data-loading-text');
            button.innerHTML = '<span class="loading"></span> ' + loadingText;
            button.disabled = true;
            
            // Re-enable after 3 seconds (fallback)
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        });
    });

    // Search functionality
    var searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            var query = this.value.toLowerCase();
            var searchResults = document.querySelectorAll('.searchable');
            
            searchResults.forEach(function(item) {
                var text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Table sorting
    var sortableHeaders = document.querySelectorAll('.sortable');
    sortableHeaders.forEach(function(header) {
        header.addEventListener('click', function() {
            var table = header.closest('table');
            var tbody = table.querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var column = Array.from(header.parentNode.children).indexOf(header);
            var isAscending = header.classList.contains('sort-asc');
            
            // Remove sort classes from all headers
            sortableHeaders.forEach(function(h) {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            
            // Add appropriate sort class
            header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
            
            // Sort rows
            rows.sort(function(a, b) {
                var aText = a.children[column].textContent.trim();
                var bText = b.children[column].textContent.trim();
                
                // Try to parse as numbers
                var aNum = parseFloat(aText);
                var bNum = parseFloat(bText);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return isAscending ? bNum - aNum : aNum - bNum;
                } else {
                    return isAscending ? bText.localeCompare(aText) : aText.localeCompare(bText);
                }
            });
            
            // Reorder rows in DOM
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });

    // Auto-refresh for dashboard
    if (document.body.classList.contains('dashboard-page')) {
        setInterval(function() {
            // Refresh specific elements instead of full page
            refreshDashboardStats();
        }, 60000); // Every minute
    }

    // Mobile menu handling
    var navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            var navbar = document.querySelector('.navbar-collapse');
            navbar.classList.toggle('show');
        });
    }

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form auto-save (for drafts)
    var autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(function(form) {
        var inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                debounce(function() {
                    saveFormData(form);
                }, 1000)();
            });
        });
        
        // Load saved data on page load
        loadFormData(form);
    });
});

// Utility functions
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

function saveFormData(form) {
    var formData = new FormData(form);
    var data = {};
    for (var [key, value] of formData.entries()) {
        data[key] = value;
    }
    localStorage.setItem('form_' + form.id, JSON.stringify(data));
}

function loadFormData(form) {
    var savedData = localStorage.getItem('form_' + form.id);
    if (savedData) {
        var data = JSON.parse(savedData);
        for (var key in data) {
            var input = form.querySelector('[name="' + key + '"]');
            if (input && input.type !== 'hidden') {
                input.value = data[key];
            }
        }
    }
}

function clearFormData(formId) {
    localStorage.removeItem('form_' + formId);
}

function refreshDashboardStats() {
    // AJAX call to refresh dashboard statistics
    fetch('/admin/api/stats')
        .then(response => response.json())
        .then(data => {
            // Update stats elements
            updateStatsElements(data);
        })
        .catch(error => {
            console.log('Stats refresh failed:', error);
        });
}

function updateStatsElements(data) {
    for (var key in data) {
        var element = document.querySelector('[data-stat="' + key + '"]');
        if (element) {
            element.textContent = data[key];
        }
    }
}

// AJAX form submission
function submitFormAjax(form, callback) {
    var formData = new FormData(form);
    
    fetch(form.action, {
        method: form.method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (callback) callback(data);
    })
    .catch(error => {
        console.error('Form submission error:', error);
        if (callback) callback({error: 'Submission failed'});
    });
}

// Status update for invites
function updateInviteStatus(playerId, eventId, status) {
    fetch('/admin/api/invite-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            player_id: playerId,
            event_id: eventId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI
            var statusElement = document.querySelector('[data-invite="' + playerId + '-' + eventId + '"]');
            if (statusElement) {
                statusElement.className = 'badge bg-' + getStatusClass(status);
                statusElement.textContent = getStatusText(status);
            }
            showNotification('Status erfolgreich aktualisiert', 'success');
        } else {
            showNotification('Fehler beim Aktualisieren des Status', 'error');
        }
    })
    .catch(error => {
        console.error('Status update error:', error);
        showNotification('Fehler beim Aktualisieren des Status', 'error');
    });
}

function getStatusClass(status) {
    var classes = {
        'pending': 'warning',
        'accepted': 'success',
        'declined': 'danger',
        'maybe': 'info'
    };
    return classes[status] || 'secondary';
}

function getStatusText(status) {
    var texts = {
        'pending': 'Ausstehend',
        'accepted': 'Zugesagt',
        'declined': 'Abgesagt',
        'maybe': 'Vielleicht'
    };
    return texts[status] || status;
}

// Notification system
function showNotification(message, type) {
    var alertClass = type === 'error' ? 'danger' : type;
    var alertHtml = '<div class="alert alert-' + alertClass + ' alert-dismissible fade show" role="alert">' +
                    message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                    '</div>';
    
    var container = document.querySelector('.container');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHtml);
        
        // Auto-hide after 3 seconds
        setTimeout(function() {
            var alert = container.querySelector('.alert');
            if (alert) {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 3000);
    }
}

// Export functions for global use
window.ClubConnect = {
    updateInviteStatus: updateInviteStatus,
    showNotification: showNotification,
    submitFormAjax: submitFormAjax,
    clearFormData: clearFormData
};
