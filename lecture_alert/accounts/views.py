from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .forms import UserLoginForm
from .models import Admin, Lecturer, Timetable  
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# LOGIN LOGIC
def login_view(request):
    if request.method == 'POST':
        print("Form submission received.")
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            
            try:
                if role == 'Admin':
                    user = Admin.objects.get(username=username)
                    print(f"Admin login attempt: {username}")
                else:
                    user = Lecturer.objects.get(username=username)
                    print(f"Lecturer login attempt: {username}")
                    
                if check_password(password, user.password):
                    print(f"Password verified for {username}")
                    
                    request.session['user_id'] = user.id
                    request.session['role'] = role
                    request.session['username'] = username
                    
                    if role == 'Admin':
                        print("Redirecting to admin dashboard")
                        return redirect('admin_dashboard')
                    else:
                        print("Redirecting to lecturer dashboard")
                        return redirect('lecturer_dashboard')
                else:
                    print("Invalid password")
                    form.add_error(None, 'Invalid credentials')
            except (Admin.DoesNotExist, Lecturer.DoesNotExist) as e:
                print(f"User not found: {e}")
                form.add_error(None, 'Invalid credentials')
        else:
            print("Form validation failed")
            print(form.errors)
    else:
        form = UserLoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def admin_view(request):
    return render(request, 'accounts/admin_dashboard.html')

def edit_view(request):
    return render(request, 'accounts/edit_lecturer.html')
#  ALL LECTURERS TABLE
def all_lecturers(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'accounts/all_lecturers.html', {'lecturers': lecturers})

# ADMIN VIEWING TIMETABLE FROM ADMIN DASHBOARD
def view_timetable(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    timetables = Timetable.objects.filter(lecturer=lecturer).order_by('date', 'start_time')
    return render(request, 'accounts/timetable.html', {
        'lecturer': lecturer,
        'timetables': timetables
    })

# ADDING TIMETABLE

def add_timetable(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    if request.method == 'POST':
        Timetable.objects.create(
            lecturer=lecturer,
            department=request.POST['department'],
            course=request.POST['course'],
            date=request.POST['date'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            venue=request.POST['venue']
        )
        return redirect('view_timetable', lecturer_id=lecturer.id)

    departments_data = {
        'Agriculture and Environmental Sciences': ['Agricultural Engineering', 'Animal Science', 'Crop Science', 'Food Science and Technology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Marketing'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education'],
        'Engineering and Architecture': ['Architecture and interior design', 'Building Technology', 'Quantity Surveying'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry'],
        'Law': ['Civil Law', 'Common Law', 'International Law'],
        'Pure And Applied Sciences': ['Microbiology', 'Chemistry', 'Mathematics & Actuarial Science', 'Physics']
    }

    return render(request, 'accounts/add_timetable.html', {
        'lecturer': lecturer,
        'departments': departments_data
    })


# EDITING TIMETABLE
def edit_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)
    departments_data = {
        'Agriculture and Environmental Sciences': ['Agricultural Engineering', 'Animal Science', 'Crop Science', 'Food Science and Technology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Marketing'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education'],
        'Engineering and Architecture': ['Architecture and interior design', 'Building Technology', 'Quantity Surveying'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry'],
        'Law': ['Civil Law', 'Common Law', 'International Law'],
        'Pure And Applied Sciences': ['Microbiology', 'Chemistry', 'Mathematics & Actuarial Science', 'Physics']
    }
    
    context = {
        'timetable': timetable,
        'departments': departments_data,
        'departments_json': json.dumps(departments_data)
    }
    return render(request, 'accounts/edit_timetable.html', context)


def delete_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id)
    lecturer_id = timetable.lecturer.id
    timetable.delete()
    return redirect('view_timetable', lecturer_id=lecturer_id)

def lecturer_view(request):
    return render(request, 'accounts/lecturer_dashboard.html')

# REGISTRATION LOGIC

def register(request):
    if request.method == 'POST':
        print("Form submission received.")
        
        # Get form data
        data = {
            'email': request.POST.get('email'),
            'username': request.POST.get('username'),
            'fullname': request.POST.get('fullname'),
            'phone': request.POST.get('phone'),
            'role': request.POST.get('role'),
            'password': request.POST.get('password')
        }
        
        # Validate required fields
        required_fields = ['email', 'username', 'fullname', 'password', 'role']
        if not all(data.get(field) for field in required_fields):
            messages.error(request, 'All fields are required')
            return render(request, 'accounts/admin_dashboard.html')

        try:
            if data['role'] == 'Admin':
                admin = Admin.objects.create(
                    email=data['email'],
                    username=data['username'],
                    fullname=data['fullname'],
                    phone=data['phone'],
                    password=make_password(data['password'])
                )
                messages.success(request, 'Admin created successfully')
            else:
                lecturer = Lecturer.objects.create(
                    email=data['email'],
                    username=data['username'],
                    fullname=data['fullname'],
                    phone=data['phone'],
                    department=request.POST.get('department'),
                    courses=request.POST.get('courses'),
                    password=make_password(data['password'])
                )
                messages.success(request, 'Lecturer created successfully')
            
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, str(e))
            
    return render(request, 'accounts/admin_dashboard.html')

# LECTURER LOGIN LOGIC
def lecturer_dashboard(request):
    print("Lecturer dashboard view called")
    user_id = request.session.get('user_id')
    role = request.session.get('role')
    
    if not user_id or role != 'Lecturer':
        print("Invalid session, redirecting to login")
        return redirect('login')
    
    try:
        lecturer = Lecturer.objects.get(id=user_id)
        timetables = Timetable.objects.filter(lecturer=lecturer).order_by('date', 'start_time')
        print(f"Found {timetables.count()} timetables for {lecturer.username}")
        
        return render(request, 'accounts/lecturer_dashboard.html', {
            'lecturer': lecturer,
            'timetables': timetables
        })
    except Lecturer.DoesNotExist:
        print("Lecturer not found")
        return redirect('login')

# RETRIEVING ALL LECTURERS FOR ADMIN LANDING PAGE
@ensure_csrf_cookie
def admin_dashboard(request):
    lecturers = Lecturer.objects.all()
    return render(request, 'accounts/admin_dashboard.html', {'lecturers': lecturers})

@require_POST
def delete_lecturer(request, lecturer_id):
    try:
        lecturer = Lecturer.objects.get(id=lecturer_id)
        lecturer.delete()
        return JsonResponse({'status': 'success'})
    except Lecturer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lecturer not found'}, status=404)

# EDIT LECTURER
def edit_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    
    if request.method == 'POST':
        try:
            lecturer.username = request.POST['username']  # Add username field
            lecturer.fullname = request.POST['fullname']
            lecturer.email = request.POST['email']
            lecturer.phone = request.POST['phone']
            lecturer.department = request.POST['department']
            lecturer.courses = request.POST['course']
            lecturer.save()
            
            messages.success(request, 'Lecturer updated successfully')
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, str(e))
    
    departments_data = {
        'Agriculture and Environmental Sciences': ['Agricultural Engineering', 'Animal Science', 'Crop Science', 'Food Science and Technology'],
        'Business, Economics and Tourism': ['Business Administration', 'Accounting', 'Public Administration', 'Marketing'],
        'Education & Lifelong Learning': ['Educational Psychology', 'Guidance and Counselling', 'Adult Education'],
        'Engineering and Architecture': ['Architecture and interior design', 'Building Technology', 'Quantity Surveying'],
        'Health Sciences': ['Human Anatomy', 'Human Physiology', 'Medical Biochemistry'],
        'Law': ['Civil Law', 'Common Law', 'International Law'],
        'Pure And Applied Sciences': ['Microbiology', 'Chemistry', 'Mathematics & Actuarial Science', 'Physics']
    }

    context = {
        'lecturer': lecturer,
        'departments': departments_data,
        'departments_json': json.dumps(departments_data),
        'current_department': lecturer.department,
        'current_course': lecturer.courses
    }
    
    return render(request, 'accounts/edit_lecturer.html', context)
#VIEWING ALL ADMINS
def all_admins(request):
    if not request.session.get('user_id') or request.session.get('role') != 'Admin':
        return redirect('login')
    
    admins = Admin.objects.all().order_by('fullname')
    return render(request, 'accounts/all_admins.html', {'admins': admins})
