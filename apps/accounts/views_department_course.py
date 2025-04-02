from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Department, Course


def departments_courses(request):
    departments = Department.objects.prefetch_related('courses').all()
    # Get expanded departments from session
    expanded_departments = request.session.get('expanded_departments', [])
    
    context = {
        'departments': departments,
        'expanded_departments': expanded_departments,
        'messages': messages.get_messages(request)  # Get messages for this request
    }
    return render(request, 'accounts/department_courses.html', context)


def toggle_department(request, department_id):
    """Toggle department expansion state"""
    if request.method == 'POST':
        # Get current list of expanded departments
        expanded_departments = request.session.get('expanded_departments', [])
        
        # Toggle department state
        if department_id in expanded_departments:
            expanded_departments.remove(department_id)
        else:
            expanded_departments.append(department_id)
        
        # Save back to session
        request.session['expanded_departments'] = expanded_departments
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'expanded': department_id in expanded_departments})
    
    return redirect('departments_courses')


def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('department_name')
        code = request.POST.get('department_code')
        if Department.objects.filter(name=name).exists():
            messages.error(request, f'Department "{name}" already exists.')
        else:
            Department.objects.create(name=name, code=code)
            messages.success(request, f'Department "{name}" added successfully.')
    return redirect('departments_courses')


def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('course_name')
        code = request.POST.get('course_code')
        department_id = request.POST.get('department_id')
        department = Department.objects.get(id=department_id)

        if Course.objects.filter(name=name, department=department).exists():
            messages.error(request, f'Course "{name}" already exists in the department "{department.name}".')
        else:
            Course.objects.create(name=name, code=code, department=department)
            messages.success(request, f'Course "{name}" added successfully to the department "{department.name}".')
    return redirect('departments_courses')


def delete_department(request, department_id):
    if request.method == 'POST':
        try:
            department = get_object_or_404(Department, id=department_id)
            name = department.name
            department.delete()
            messages.success(request, f'Department "{name}" and all its associated courses have been deleted.')
        except Department.DoesNotExist:
            messages.error(request, 'The department you are trying to delete does not exist.')
    return redirect('departments_courses')


def delete_course(request, course_id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=course_id)
            name = course.name
            course.delete()
            messages.success(request, f'Course "{name}" has been deleted successfully.')
        except Course.DoesNotExist:
            messages.error(request, 'The course you are trying to delete does not exist.')
    return redirect('departments_courses')


def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        name = request.POST.get('department_name')
        code = request.POST.get('department_code')

        if Department.objects.filter(name=name).exclude(id=department_id).exists():
            messages.error(request, f'Department "{name}" already exists.')
        else:
            department.name = name
            department.code = code
            department.save()
            messages.success(request, f'Department "{name}" updated successfully.')
            return redirect('departments_courses')

    return render(request, 'accounts/edit_department.html', {'department': department})


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        name = request.POST.get('course_name')
        code = request.POST.get('course_code')
        department_id = request.POST.get('department_id')
        department = get_object_or_404(Department, id=department_id)

        # Check if another course with the same name exists in the same department
        if Course.objects.filter(name=name, department=department).exclude(id=course_id).exists():
            messages.error(request, f'Course "{name}" already exists in the department "{department.name}".')
        else:
            course.name = name
            course.code = code
            course.department = department
            course.save()
            messages.success(request, f'Course "{name}" updated successfully.')
            return redirect('departments_courses')

    return render(request, 'accounts/edit_course.html', {'course': course, 'departments': Department.objects.all()})


def dismiss_message(request, message_id):
    """Handle AJAX request to dismiss a message"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Remove message from session
        storage = messages.get_messages(request)
        for message in storage:
            if str(message.id) == str(message_id):
                storage.used = False  # Mark as unused so it won't be cleared
                return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)



def update_courses(request, department_id):
    """Return courses for a given department as JSON"""
    try:
        courses = Course.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse({
            'success': True,
            'courses': list(courses)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
