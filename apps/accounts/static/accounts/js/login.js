document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const roleSelect = document.getElementById('role');
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    form.addEventListener('submit', function(e) {
        // Remove existing error messages
        removeErrors();

        let hasError = false;

        // Validate role
        if (!roleSelect.value) {
            showError(roleSelect, 'Please select your role');
            hasError = true;
        }

        // Validate username
        if (!username.value.trim()) {
            showError(username, 'Username is required');
            hasError = true;
        }

        // Validate password
        if (!password.value) {
            showError(password, 'Password is required');
            hasError = true;
        }

        if (hasError) {
            e.preventDefault();
        }
    });

    function showError(element, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-red-500 text-xs mt-1 error-message';
        errorDiv.textContent = message;
        element.classList.add('border-red-500');
        element.parentNode.appendChild(errorDiv);
    }

    function removeErrors() {
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        document.querySelectorAll('.border-red-500').forEach(el => {
            el.classList.remove('border-red-500');
        });
    }
});