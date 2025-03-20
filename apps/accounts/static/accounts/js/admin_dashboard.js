// Wait for the DOM to be fully loaded before running scripts
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    // Initialize mobile menu functionality
    initMobileMenu();
    
    // Initialize password strength meter
    initPasswordStrengthMeter();
    
    // Initialize role-based field visibility
    initRoleFieldToggle();
    
    // Initialize alert dismissal functionality
    initAlertSystem();
});

console.log('Admin dashboard JS loaded successfully');

/**
 * Form validation for staff registration
 * Used in the form's onsubmit attribute
 */
function validateForm() {
    console.log('Form validation running');
    const role = document.getElementById('roleSelect').value;
    const department = document.getElementById('departmentSelect').value;
    const password = document.getElementById('password').value;
    
    let isValid = true;
    let errors = [];
    
    if (!role) {
        errors.push('Please select a role');
        isValid = false;
    }
    
    if (!department) {
        errors.push('Please select a department');
        isValid = false;
    }
    
    if (password.length < 8) {
        errors.push('Password must be at least 8 characters');
        isValid = false;
    }
    
    if (!isValid) {
        const errorDiv = document.getElementById('form-errors');
        errorDiv.innerHTML = errors.map(err => `<p>• ${err}</p>`).join('');
        errorDiv.classList.remove('hidden');
        window.scrollTo({top: 0, behavior: 'smooth'});
        return false;
    }
    
    return true;
}

/**
 * Mobile menu toggle functionality
 */
function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
         
        });
    }
}

/**
 * Password strength meter functionality
 */
function initPasswordStrengthMeter() {
    const password = document.getElementById('password');
    const strengthIndicator = document.getElementById('password-strength');
    
    if (password && strengthIndicator) {
        password.addEventListener('input', function() {
            const value = this.value;
            
            if (value.length === 0) {
                strengthIndicator.className = 'h-1 mt-2 rounded-full bg-gray-200';
                return;
            }
            
            // Simple strength calculation
            let strength = 0;
            
            // Length check
            if (value.length >= 8) strength += 1;
            if (value.length >= 12) strength += 1;
            
            // Contains number
            if (/\d/.test(value)) strength += 1;
            
            // Contains special char
            if (/[^A-Za-z0-9]/.test(value)) strength += 1;
            
            // Mixed case
            if (/[A-Z]/.test(value) && /[a-z]/.test(value)) strength += 1;
            
            // Set indicator class
            if (strength <= 2) {
                strengthIndicator.className = 'h-1 mt-2 rounded-full bg-red-500 w-1/3';
            } else if (strength <= 4) {
                strengthIndicator.className = 'h-1 mt-2 rounded-full bg-yellow-500 w-2/3';
            } else {
                strengthIndicator.className = 'h-1 mt-2 rounded-full bg-green-500 w-full';
            }
        });
    }
}

/**
 * Role-based field visibility functionality
 */
function initRoleFieldToggle() {
    const roleSelect = document.getElementById('roleSelect');
    const coursesContainer = document.getElementById('courses-container');
    
    if (roleSelect && coursesContainer) {
        roleSelect.addEventListener('change', function() {
            if (this.value === 'Lecturer') {
                coursesContainer.classList.remove('hidden');
            } else {
                coursesContainer.classList.add('hidden');
            }
        });
        
        // Set initial state based on current value
        if (roleSelect.value === 'Lecturer') {
            coursesContainer.classList.remove('hidden');
        } else if (roleSelect.value !== '') {
            coursesContainer.classList.add('hidden');
        }
    }
}

/**
 * Alert system initialization and management
 */
function initAlertSystem() {
    console.log('Initializing alert system');
    
    // Manual close button functionality
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    console.log('Found alert close buttons:', alertCloseButtons.length);
    
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Close button clicked');
            // Use closest() with the correct parent selector
            const alert = this.closest('[role="alert"]');
            dismissAlert(alert);
        });
    });
    
    // Auto dismiss alerts
    const alerts = document.querySelectorAll('[role="alert"]');
    console.log('Found alerts:', alerts.length);
    
    alerts.forEach((alert, index) => {
        setTimeout(() => {
            dismissAlert(alert);
        }, 5000 + (index * 1000)); // 5 seconds + staggered timing
    });
}

/**
 * Helper function to dismiss an alert with animation
 */
function dismissAlert(alert) {
    if (!alert) {
        console.log('No alert to dismiss');
        return;
    }
    
    console.log('Dismissing alert:', alert);
    
    // For debugging
    if (!alert.classList) {
        console.error('Alert element has no classList property:', alert);
        return;
    }
    
    // Add transition style directly if not already in CSS
    alert.style.transition = 'opacity 300ms ease-in-out';
    alert.style.opacity = '0';
    
    setTimeout(() => {
        if (alert.parentElement) {
            alert.parentElement.removeChild(alert);
        }
    }, 300);
}

