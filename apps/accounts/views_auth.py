from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Admin, Lecturer
from django.contrib.auth.hashers import check_password

def login_view(request):
    # Redirect if already logged in
    if request.session.get('user_type') == 'lecturer':
        return redirect('lecturer_dashboard')
    elif request.session.get('user_type') == 'admin':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        remember_me = request.POST.get('remember_me', False)

        # Debugging login attempt
        print(f"Login attempt - Username: {username}, Role: {role}")

        # Check if all fields are filled
        if not all([username, password, role]):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'accounts/login.html')

        try:
            if role == 'Admin':
                # Authenticate against Admin model
                try:
                    admin = Admin.objects.get(username=username)
                    if check_password(password, admin.password):  # Verify password
                        # Login successful
                        request.session['user_type'] = 'admin'
                        request.session['user_id'] = admin.id
                        if not remember_me:
                            request.session.set_expiry(0)  # Session expires on browser close
                        messages.success(request, f'Welcome back, {admin.fullname}!')
                        print(f"Admin login successful: {admin.fullname}")
                        return redirect('admin_dashboard')
                    else:
                        messages.error(request, 'Invalid username or password')
                except Admin.DoesNotExist:
                    messages.error(request, 'Admin account not found')

            elif role == 'Lecturer':
                # Authenticate against Lecturer model
                try:
                    lecturer = Lecturer.objects.get(username=username)
                    if check_password(password, lecturer.password):  # Verify password
                        # Login successful
                        request.session['user_type'] = 'lecturer'
                        request.session['user_id'] = lecturer.id
                        if not remember_me:
                            request.session.set_expiry(0)  # Session expires on browser close
                        messages.success(request, f'Welcome back, {lecturer.fullname}!')
                        print(f"Lecturer login successful: {lecturer.fullname}")
                        return redirect('lecturer_dashboard')
                    else:
                        messages.error(request, 'Invalid username or password')
                except Lecturer.DoesNotExist:
                    messages.error(request, 'Lecturer account not found')

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            messages.error(request, 'An error occurred during login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    user_type = request.session.get('user_type', '')
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out successfully')
    print(f"User logged out - Type: {user_type}")  # Debug print
    return redirect('login')



