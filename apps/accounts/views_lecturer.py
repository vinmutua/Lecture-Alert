from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, date
from .models import Timetable

@login_required
def lecturer_dashboard(request):
    # Get current lecturer
    lecturer = request.user.lecturer
    
    # Get today's date
    today = date.today()
    
    # Get upcoming and today's lectures
    timetables = Timetable.objects.filter(
        lecturer=lecturer,
        date__gte=today
    ).select_related(
        'department', 
        'course'
    ).order_by('date', 'start_time')
    
    context = {
        'lecturer': lecturer,
        'timetables': timetables,
    }
    
    return render(request, 'accounts/lecturer_dashboard.html', context)

