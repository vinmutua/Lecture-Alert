document.addEventListener('DOMContentLoaded', function() {
    const departmentSelect = document.getElementById('departmentSelect1');
    const coursesSelect = document.getElementById('coursesSelect1');
    const currentCourse = coursesSelect.getAttribute('data-current-course');
    const departmentsData = JSON.parse(document.getElementById('departments-data').textContent);

    function updateCourses(department) {
        const courses = departmentsData[department] || [];
        coursesSelect.innerHTML = '';
        
        if (currentCourse) {
            const option = document.createElement('option');
            option.value = currentCourse;
            option.textContent = currentCourse;
            option.selected = true;
            coursesSelect.appendChild(option);
        }

        courses.forEach(course => {
            if (course !== currentCourse) {
                const option = document.createElement('option');
                option.value = course;
                option.textContent = course;
                coursesSelect.appendChild(option);
            }
        });
    }

    if (departmentSelect.value) {
        updateCourses(departmentSelect.value);
    }

    departmentSelect.addEventListener('change', function() {
        updateCourses(this.value);
    });
});