

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, setting up accordion');
    // Department accordion toggle
    const departmentHeaders = document.querySelectorAll('.department-header');
    
    departmentHeaders.forEach(header => {
        header.addEventListener('click', function() {
            console.log('Click detected on department header');
            // Get the next sibling element which should be the content div
            const content = this.nextElementSibling;
            
            // Toggle visibility
            if (content.classList.contains('hidden')) {
                content.classList.remove('hidden');
            } else {
                content.classList.add('hidden');
            }
            console.log('Hidden class toggled, current classes:', content.className);
            // Toggle icon rotation
            const icon = this.querySelector('i');
            icon.classList.toggle('rotate-180');
        });
    });
    
    // Delete Department
    const deleteDepartmentButtons = document.querySelectorAll('.delete-department');
    deleteDepartmentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const departmentId = this.dataset.departmentId;
            
            // Set up modal
            document.getElementById('modal-title').textContent = 'Delete Department';
            document.getElementById('modal-message').textContent = 'Are you sure you want to delete this department? This will also delete all courses associated with this department.';
            document.getElementById('deleteForm').action = `/delete-department/${departmentId}/`;
            
            // Show modal
            document.getElementById('deleteModal').classList.remove('hidden');
        });
    });

    // Delete Course
    const deleteCourseButtons = document.querySelectorAll('.delete-course');
    deleteCourseButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const courseId = this.dataset.courseId;
            
            // Set up modal
            document.getElementById('modal-title').textContent = 'Delete Course';
            document.getElementById('modal-message').textContent = 'Are you sure you want to delete this course?';
            document.getElementById('deleteForm').action = `/delete-course/${courseId}/`;
            
            // Show modal
            document.getElementById('deleteModal').classList.remove('hidden');
        });
    });

    // Cancel delete
    document.getElementById('cancelDelete').addEventListener('click', function() {
        document.getElementById('deleteModal').classList.add('hidden');
    });
});