from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.db import transaction

from .models import Lecturer, Timetable, Department, Course


def view_timetable(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    timetables = Timetable.objects.filter(lecturer=lecturer).select_related(
        'department', 'course'
    ).order_by('date', 'start_time')
    
    return render(request, 'accounts/timetable.html', {
        'lecturer': lecturer,
        'timetables': timetables
    })


@transaction.atomic
def add_timetable(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    departments = Department.objects.all()
    selected_department = None
    available_courses = []
    form_data = {}
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(f"Form type: {form_type}")  # Debug line
        print(f"POST data: {request.POST}")  # Debug line
        
        if form_type == 'department_select':
            # Handle department selection
            department_id = request.POST.get('department')
            if department_id:
                selected_department = int(department_id)
                available_courses = Course.objects.filter(department_id=selected_department)
                form_data = request.POST.dict()
        elif form_type == 'timetable_submit':
            try:
                # Create new timetable entry
                timetable = Timetable.objects.create(
                    lecturer=lecturer,
                    department_id=request.POST.get('department'),
                    course_id=request.POST.get('course'),
                    date=request.POST.get('date'),
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    venue=request.POST.get('venue')
                )
                messages.success(request, 'Timetable entry added successfully')
                return redirect('view_timetable', lecturer_id=lecturer.id)
            except Exception as e:
                print(f"Error creating timetable: {str(e)}")  # Debug line
                messages.error(request, f'Error adding timetable: {str(e)}')
                form_data = request.POST.dict()
                if form_data.get('department'):
                    selected_department = int(form_data['department'])
                    available_courses = Course.objects.filter(department_id=selected_department)
    
    context = {
        'lecturer': lecturer,
        'departments': departments,
        'selected_department': selected_department,
        'available_courses': available_courses,
        'form_data': form_data
    }
    
    return render(request, 'accounts/add_timetable.html', context)



@transaction.atomic
def edit_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)
    departments = Department.objects.all()
    selected_department = timetable.department.id if timetable.department else None
    available_courses = []
    form_data = {}

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(f"Form type: {form_type}")  # Debug print
        print(f"POST data: {request.POST}")  # Debug print
        
        if form_type == 'department_select':
            # Handle department selection
            department_id = request.POST.get('department')
            if department_id:
                selected_department = int(department_id)
                available_courses = Course.objects.filter(department_id=selected_department)
                form_data = request.POST.dict()
        elif form_type == 'timetable_update':  # Check for the correct form type
            try:
                # Update timetable
                department_id = request.POST.get('department')
                course_id = request.POST.get('course')
                
                if not department_id or not course_id:
                    raise ValueError("Department and course are required")
                
                timetable.department_id = department_id
                timetable.course_id = course_id
                timetable.date = request.POST.get('date')
                timetable.start_time = request.POST.get('start_time')
                timetable.end_time = request.POST.get('end_time')
                timetable.venue = request.POST.get('venue')
                timetable.save()
                
                print(f"Timetable updated successfully: {timetable.id}")  # Debug print
                messages.success(request, 'Timetable updated successfully')
                return redirect('view_timetable', lecturer_id=timetable.lecturer.id)
            except Exception as e:
                print(f"Error updating timetable: {str(e)}")  # Debug print
                messages.error(request, f'Error updating timetable: {str(e)}')
                form_data = request.POST.dict()
                if department_id:
                    selected_department = int(department_id)
                    available_courses = Course.objects.filter(department_id=selected_department)
    
    # Load initial courses based on selected department
    if selected_department:
        available_courses = Course.objects.filter(department_id=selected_department)
    
    context = {
        'timetable': timetable,
        'departments': departments,
        'selected_department': selected_department,
        'available_courses': available_courses,
        'selected_course': timetable.course.id if timetable.course else None,
        'form_data': form_data
    }
    
    return render(request, 'accounts/edit_timetable.html', context)


@transaction.atomic
def delete_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)
    lecturer_id = timetable.lecturer.id
    
    try:
        timetable.delete()
        messages.success(request, 'Timetable entry deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting timetable: {str(e)}')
    
    return redirect('view_timetable', lecturer_id=lecturer_id)
