from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Admin, Lecturer

def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        user_type = request.session.get('user_type')
        if user_type == 'lecturer':
            return redirect('lecturer_dashboard')
        elif user_type == 'admin':
            return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        remember_me = request.POST.get('remember_me', False)

        print(f"Login attempt - Username: {username}, Role: {role}")  # Debug print

        if not all([username, password, role]):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'accounts/login.html')

        try:
            # First authenticate with Django's auth system
            user = authenticate(username=username, password=password)

            if user is not None:
                if role == 'Admin':
                    # Verify admin exists and matches user
                    try:
                        admin = Admin.objects.get(user=user)
                        login(request, user)
                        request.session['user_type'] = 'admin'
                        request.session['user_id'] = admin.id
                        if not remember_me:
                            request.session.set_expiry(0)
                        messages.success(request, f'Welcome back, {admin.fullname}!')
                        print(f"Admin login successful: {admin.fullname}")  # Debug print
                        return redirect('admin_dashboard')
                    except Admin.DoesNotExist:
                        messages.error(request, 'User is not registered as an admin')

                elif role == 'Lecturer':
                    # Verify lecturer exists and matches user
                    try:
                        lecturer = Lecturer.objects.get(user=user)
                        login(request, user)
                        request.session['user_type'] = 'lecturer'
                        request.session['user_id'] = lecturer.id
                        if not remember_me:
                            request.session.set_expiry(0)
                        messages.success(request, f'Welcome back, {lecturer.fullname}!')
                        print(f"Lecturer login successful: {lecturer.fullname}")  # Debug print
                        return redirect('lecturer_dashboard')
                    except Lecturer.DoesNotExist:
                        messages.error(request, 'User is not registered as a lecturer')
            else:
                messages.error(request, 'Invalid username or password')

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



