import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Admin, Lecturer, Department, Course
from .forms import AdminRegistrationForm, LecturerRegistrationForm, LecturerUpdateForm, LecturerForm
from django.core.cache import cache

logger = logging.getLogger(__name__)


def admin_dashboard(request):
    # Fetch all departments and their courses
    departments = Department.objects.prefetch_related('courses')
    departments_json = {
        str(department.id): [
            {"id": str(course.id), "name": course.name}
            for course in department.courses.all()
        ]
        for department in departments
    }

    # Fetch all lecturers
    lecturers = Lecturer.objects.select_related('department').prefetch_related('courses').order_by('-created_at')

    return render(request, 'accounts/admin_dashboard.html', {
        'departments': departments,
        'departments_json': departments_json,
        'lecturers': lecturers,
    })



@transaction.atomic
def delete_lecturer(request, lecturer_id):
    if request.method == 'POST':
        try:
            lecturer = get_object_or_404(Lecturer, id=lecturer_id)
            name = lecturer.fullname
            lecturer.delete()
            messages.success(request, f'Lecturer {name} has been deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting lecturer: {str(e)}')

    return redirect('all_lecturers')


@transaction.atomic
def register_lecturer(request):
    departments = Department.objects.all()
    selected_department = None
    available_courses = []
    print(f"Request method: {request.method}")  # Debug line
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(f"Form type: {form_type}")  # Debug line
        print(f"POST data: {request.POST}")  # Debug line
        
        if form_type == 'department_select':
            department_id = request.POST.get('department')
            if department_id:
                selected_department = int(department_id)
                available_courses = Course.objects.filter(department_id=selected_department)
        else:
            try:
                # Create new lecturer
                lecturer = Lecturer(
                    fullname=request.POST.get('fullname'),
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    department_id=request.POST.get('department')
                )
                
                # Set password
                password = request.POST.get('password')
                if password:
                    lecturer.set_password(password)
                
                # Save lecturer
                lecturer.save()
                
                # Add course
                course_id = request.POST.get('courses')
                if course_id:
                    lecturer.courses.add(course_id)
                
                messages.success(request, f'Lecturer {lecturer.fullname} registered successfully')
                return redirect('admin_dashboard')
                
            except Exception as e:
                print(f"Error: {str(e)}")  # Debug line
                messages.error(request, f'Error registering lecturer: {str(e)}')
                
                # Keep selected department and courses on error
                if request.POST.get('department'):
                    selected_department = int(request.POST.get('department'))
                    available_courses = Course.objects.filter(department_id=selected_department)

    context = {
        'departments': departments,
        'selected_department': selected_department,
        'available_courses': available_courses,
        'lecturers': Lecturer.objects.all().select_related('department'),
        'form_data': request.POST if request.method == 'POST' else None
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


@transaction.atomic
def edit_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'department_select':
            # Handle department change
            department_id = request.POST.get('department')
            available_courses = Course.objects.filter(department_id=department_id)
            return JsonResponse({
                'courses': list(available_courses.values('id', 'name'))
            })
        else:
            try:
                # Update lecturer details
                lecturer.fullname = request.POST.get('fullname')
                lecturer.username = request.POST.get('username')
                lecturer.email = request.POST.get('email')
                lecturer.phone = request.POST.get('phone')
                lecturer.department_id = request.POST.get('department')
                
                # Update password if provided
                password = request.POST.get('password')
                if password:
                    lecturer.set_password(password)
                
                # Save lecturer
                lecturer.save()
                
                # Update course
                course_id = request.POST.get('courses')
                if course_id:
                    lecturer.courses.set([course_id])
                
                messages.success(request, f'Lecturer {lecturer.fullname} updated successfully')
                return redirect('all_lecturers')
                
            except Exception as e:
                print(f"Error updating lecturer: {str(e)}")  # Debug line
                messages.error(request, f'Error updating lecturer: {str(e)}')
    
    # For GET request, prepare forms with current data
    departments = Department.objects.all()
    available_courses = Course.objects.filter(department=lecturer.department) if lecturer.department else []
    
    context = {
        'lecturer': lecturer,
        'departments': departments,
        'available_courses': available_courses,
        'current_course': lecturer.courses.first()
    }
    
    return render(request, 'accounts/edit_lecturer.html', context)


def all_lecturers(request):
    # Fetch all lecturers from the database
    lecturers = Lecturer.objects.select_related('department').prefetch_related('courses').order_by('-created_at')

    # Count the total number of lecturers
    lecturer_count = lecturers.count()

    # Render the template with the list of lecturers
    return render(request, 'accounts/all_lecturers.html', {
        'lecturers': lecturers,
        'lecturer_count': lecturer_count,
    })


@transaction.atomic
def add_admin(request):
    """Handle adding new administrators"""
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            try:
                admin = form.save(commit=False)
                admin.set_password(form.cleaned_data['password'])
                admin.save()
                messages.success(request, f'Administrator "{admin.fullname}" added successfully')
                return redirect('all_admins')
            except Exception as e:
                messages.error(request, f'Error saving administrator: {str(e)}')
    else:
        # Create a new empty form
        form = AdminRegistrationForm()

    return render(request, 'accounts/add_admin.html', {
        'form': form
    })


@transaction.atomic
def update_admin(request, admin_id):
    """Handle updating existing administrators"""
    admin = get_object_or_404(Admin, id=admin_id)
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST, instance=admin)
        if form.is_valid():
            try:
                admin = form.save(commit=False)
                # Only update password if provided
                password = form.cleaned_data.get('password')
                if password:
                    admin.set_password(password)
                admin.save()
                logger.info(f"Administrator {admin.username} updated successfully")
                messages.success(request, f'Administrator "{admin.fullname}" updated successfully')
                return redirect('all_admins')
            except Exception as e:
                logger.error(f"Error updating administrator: {str(e)}")
                messages.error(request, f'Error updating administrator: {str(e)}')
    else:
        # For GET request, initialize form with admin's data
        form = AdminRegistrationForm(instance=admin)
        logger.info(f"Loading edit form for administrator {admin.username}")

    return render(request, 'accounts/edit_admin.html', {
        'form': form,
        'admin': admin
    })


@transaction.atomic
def delete_admin(request, admin_id):
    """Handle deleting administrators"""
    if request.method == 'POST':
        try:
            admin = get_object_or_404(Admin, id=admin_id)
            # Prevent deletion of super admin
            if admin.is_super_admin:
                messages.error(request, 'Super administrators cannot be deleted.')
                return redirect('all_admins')
            
            name = admin.fullname
            admin.delete()
            messages.success(request, f'Administrator "{name}" deleted successfully')
        except Exception as e:
            logger.error(f"Error deleting admin: {str(e)}")
            messages.error(request, f'Error deleting administrator: {str(e)}')
    
    return redirect('all_admins')


@transaction.atomic
def all_admins(request):
    """List all administrators"""
    admins = Admin.objects.all().order_by('-created_at')
    return render(request, 'accounts/all_admins.html', {
        'admins': admins
    })




