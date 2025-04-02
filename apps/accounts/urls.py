from django.urls import path
from .views_auth import login_view, logout_view
from .views_admin import (
    admin_dashboard, all_admins, update_admin, 
    delete_admin, register_lecturer, all_lecturers, 
    delete_lecturer, add_admin, update_admin, edit_lecturer,
) 
from .views_lecturer import lecturer_dashboard
from .views_timetable import (
    view_timetable, add_timetable, 
    edit_timetable, delete_timetable,
)
from .views_department_course import (
    departments_courses, add_department, add_course,
    delete_department, delete_course, edit_department,
    edit_course, toggle_department, dismiss_message, update_courses, 
   
)

urlpatterns = [
    # LOGIN URL
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # DASHBOARD URLS
    path('lecturer_dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),

    # LECTURER MANAGEMENT URLS
    path('register-lecturer/', register_lecturer, name='register_lecturer'),
    path('lecturer/edit/<int:lecturer_id>/', edit_lecturer, name='edit_lecturer'),

    # TIMETABLE MANAGEMENT URLS
    path('timetable/<int:lecturer_id>/', view_timetable, name='view_timetable'),
    path('add-timetable/<int:lecturer_id>/', add_timetable, name='add_timetable'),
    path('edit-timetable/<int:timetable_id>/', edit_timetable, name='edit_timetable'),
    path('delete-timetable/<int:timetable_id>/', delete_timetable, name='delete_timetable'),

    # ADMIN MANAGEMENT URLS
    path('all-admins/', all_admins, name='all_admins'),
    path('add-admin/', add_admin, name='add_admin'),
    path('update-admin/<int:admin_id>/', update_admin, name='update_admin'),
    path('delete-admin/<int:admin_id>/', delete_admin, name='delete_admin'),

    path('lecturers/', all_lecturers, name='all_lecturers'),
    path('delete-lecturer/<int:lecturer_id>/', delete_lecturer, name='delete_lecturer'),

    # DEPARTMENT AND COURSE MANAGEMENT URLS
    path('add-department/', add_department, name='add_department'),
    path('delete-department/<int:department_id>/', delete_department, name='delete_department'),
    path('edit-department/<int:department_id>/', edit_department, name='edit_department'),
    path('add-course/', add_course, name='add_course'),
    path('departments-courses/', departments_courses, name='departments_courses'),
    path('delete-course/<int:course_id>/', delete_course, name='delete_course'),
    path('edit-course/<int:course_id>/', edit_course, name='edit_course'),
    path('toggle-department/<int:department_id>/', toggle_department, name='toggle_department'),
    path('dismiss-message/<int:message_id>/', dismiss_message, name='dismiss_message'),
    path('update-courses/<int:department_id>/', update_courses, name='update_courses'),
]
