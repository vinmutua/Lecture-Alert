document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin dashboard JS loaded'); // Confirm script loading

    // FORM DEPARTMENTS AND COURSES START

    const roleSelect = document.getElementById('roleSelect');
    const departmentSelect = document.getElementById('departmentSelect');
    const coursesSelect = document.getElementById('coursesSelect');

    const coursesOptions = {
        'Agriculture and Environmental Sciences': ['Agricultural Economics', 'Animal Science', 'Agricultural Sciences and Technology', 'Crop Science', 'Food Science and Technology', 'Forestry and Wildlife', 'Horticulture', 'Soil Science', 'Water Resources Management and Agro-meteorology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Purchasing and Supply', 'Tourism and Hospitality Management', 'Marketing', 'Banking and Finance'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education', 'Curriculum Studies', 'Educational Management', 'Educational Technology', 'Science Education', 'Social Science Education', 'Language Education', 'Physical and Health Education', 'Vocational and Technical Education', 'Special Education', 'Early Childhood Education', 'Library and Information Science'],
        'Engineering and Architecture': ['Architecture and Interior Design', 'Building Technology', 'Quantity Surveying', 'Urban and Regional Planning', 'Surveying and Geoinformatics', 'Textile Design and Technology'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry', 'Medical Laboratory Science', 'Nursing Science', 'Physiotherapy', 'Radiography', 'Human Nutrition and Dietetics'],
        'Law': ['Civil Law', 'Common Law', 'International Law', 'Private Law', 'Public Law', 'Islamic Law'],
        'Pure And Applied Sciences': ['Microbiology and Biotechnology', 'Chemistry', 'Mathematics & Actuarial Science', 'Plant Sciences', 'Computing & Information Science', 'Physics']
    };

    roleSelect.addEventListener('change', function() {
        const selectedRole = roleSelect.value;
        if (selectedRole === 'Admin') {
            departmentSelect.disabled = true;
            coursesSelect.disabled = true;
        } else {
            departmentSelect.disabled = false;
            coursesSelect.disabled = false;
        }
    });

    departmentSelect.addEventListener('change', function() {
        const selectedValue = departmentSelect.value;
        const options = coursesOptions[selectedValue] || [];

        // Clear previous options
        coursesSelect.innerHTML = '<option value="" disabled selected>Courses</option>';

        // Add new options
        options.forEach(course => {
            const option = document.createElement('option');
            option.value = course;
            option.textContent = course;
            coursesSelect.appendChild(option);
        });
    });
// FORM DEPARTMENTS AND COURSES END

    // FORM VALIDATION START
  
    window.validateForm = function() {
        const email = document.querySelector('input[name="email"]').value;
        const username = document.querySelector('input[name="username"]').value;
        const fullname = document.querySelector('input[name="fullname"]').value;
        const role = document.querySelector('select[name="role"]').value;
        const password = document.querySelector('input[name="password"]').value;
        const phone = document.querySelector('input[name="phone"]').value;

        // Required fields validation
        if (!email || !username || !fullname || !role || !password || !phone) {
            alert('All fields are required');
            return false;
        }

        // Email validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert('Please enter a valid email address');
            return false;
        }

        // Phone validation
        const phonePattern = /^\d{10}$/;
        if (!phonePattern.test(phone)) {
            alert('Please enter a valid 10-digit phone number');
            return false;
        }

        // Department and courses validation for Lecturer
        if (role === 'Lecturer') {
            const department = document.querySelector('select[name="department"]').value;
            const courses = document.querySelector('select[name="courses"]').value;
            
            if (!department || !courses) {
                alert('Department and Courses are required for Lecturers');
                return false;
            }
        }

        return true;
    };

    // FORM VALIDATION END
// DELETING LECTURER START 
    document.querySelectorAll('.delete-lecturer').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this lecturer?')) {
                const lecturerId = this.dataset.lecturerId;
                fetch(`/delete-lecturer/${lecturerId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        this.closest('tr').remove();
                    }
                });
            }
        });
    });

});
