document.addEventListener('DOMContentLoaded', function() {
    const departmentSelect = document.getElementById('departmentSelect1');
    const coursesSelect = document.getElementById('coursesSelect1');
    const currentCourse = coursesSelect.value;

    console.log('DOM Loaded - Initial Values:', {
        department: departmentSelect.value,
        course: currentCourse
    });

    // Department-course mapping
    const coursesOptions = {
        'Agriculture and Environmental Sciences': ['Agricultural Engineering', 'Animal Science', 'Crop Science', 'Food Science and Technology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Marketing'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education'],
        'Engineering and Architecture': ['Architecture and interior design', 'Building Technology', 'Quantity Surveying'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry'],
        'Law': ['Civil Law', 'Common Law', 'International Law'],
        'Pure And Applied Sciences': ['Microbiology', 'Chemistry', 'Mathematics & Actuarial Science', 'Physics']
    };

    function updateCourses(department) {
        console.log('Updating courses for:', department);
        const courses = coursesOptions[department] || [];
        coursesSelect.innerHTML = '';
        courses.forEach(course => {
            const option = document.createElement('option');
            option.value = course;
            option.textContent = course;
            option.selected = (course === currentCourse);
            coursesSelect.appendChild(option);
        });
    }

    // Initial load
    if (departmentSelect.value) {
        console.log('Initial department load:', departmentSelect.value);
        updateCourses(departmentSelect.value);
    }

    // Handle department changes
    departmentSelect.addEventListener('change', function() {
        const selectedDepartment = this.value;
        console.log('Department changed to:', selectedDepartment);
        updateCourses(selectedDepartment);
    });
});