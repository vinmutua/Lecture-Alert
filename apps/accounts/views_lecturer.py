from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from django.db.models import Exists, OuterRef
from apps.notification.models import Notification
from .models import Timetable, Lecturer

def lecturer_dashboard(request):
    # Custom authentication check
    if request.session.get('user_type') != 'lecturer':
        return redirect('login')  # Redirect to login if not a lecturer

    # Get current lecturer from session
    lecturer_id = request.session.get('user_id')
    try:
        lecturer = Lecturer.objects.get(id=lecturer_id)
    except Lecturer.DoesNotExist:
        # If lecturer does not exist, clear session and redirect to login
        request.session.flush()
        return redirect('login')

    # Get today's date
    today = date.today()

    # Get upcoming and today's lectures
    timetables = Timetable.objects.filter(
        lecturer=lecturer,
        date__gte=today
    ).annotate(
        notification_sent=Exists(
            Notification.objects.filter(
                timetable=OuterRef('pk'),
                is_sent=True
            )
        )
    ).select_related('department', 'course').order_by('date', 'start_time')

    context = {
        'lecturer': lecturer,
        'timetables': timetables,
    }

    return render(request, 'accounts/lecturer_dashboard.html', context)



