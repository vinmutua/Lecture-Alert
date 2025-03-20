document.addEventListener('DOMContentLoaded', function() {
    console.log('add_timetable.js loaded');
    
    const departmentSelect = document.getElementById('departmentSelect1');
    const coursesSelect = document.getElementById('coursesSelect1');
    
    console.log('Elements found:', {
        departmentSelect: !!departmentSelect,
        coursesSelect: !!coursesSelect
    });

    const coursesOptions = {
        'Agriculture and Environmental Sciences': ['Agricultural Economics', 'Animal Science', 'Agricultural Sciences and Technology', 'Crop Science', 'Food Science and Technology', 'Forestry and Wildlife', 'Horticulture', 'Soil Science', 'Water Resources Management and Agro-meteorology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Purchasing and Supply', 'Tourism and Hospitality Management', 'Marketing', 'Banking and Finance'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education', 'Curriculum Studies', 'Educational Management', 'Educational Technology', 'Science Education', 'Social Science Education', 'Language Education', 'Physical and Health Education', 'Vocational and Technical Education', 'Special Education', 'Early Childhood Education', 'Library and Information Science'],
        'Engineering and Architecture': ['Architecture and Interior Design', 'Building Technology', 'Quantity Surveying', 'Urban and Regional Planning', 'Surveying and Geoinformatics', 'Textile Design and Technology'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry', 'Medical Laboratory Science', 'Nursing Science', 'Physiotherapy', 'Radiography', 'Human Nutrition and Dietetics'],
        'Law': ['Civil Law', 'Common Law', 'International Law', 'Private Law', 'Public Law', 'Islamic Law'],
        'Pure And Applied Sciences': ['Microbiology and Biotechnology', 'Chemistry', 'Mathematics & Actuarial Science', 'Plant Sciences', 'Computing & Information Science', 'Physics']
    };

    departmentSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        console.log('Selected department:', selectedValue);
        
        const options = coursesOptions[selectedValue] || [];
        console.log('Available courses:', options);

        coursesSelect.innerHTML = '<option value="" disabled selected>Courses</option>';
        
        options.forEach(course => {
            const option = document.createElement('option');
            option.value = course;
            option.textContent = course;
            coursesSelect.appendChild(option);
            console.log('Added course:', course);
        });
    });
});