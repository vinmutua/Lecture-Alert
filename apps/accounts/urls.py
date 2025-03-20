from django.urls import path
from . import views

urlpatterns = [
    # LOGIN URL
    path('', views.login_view, name='login'),
    # REGISTER URL
    path('register/', views.register, name='register'),
    # LECTURER DASHBOARD URL
    path('lecturer_dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    # ADMIN DASHBOARD URL
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # ALL LECTURERS URL
    path('lecturers/', views.all_lecturers, name='all_lecturers'),
    # INDIVIDUAL LECTURER TIMETABLE URL
    path('timetable/<int:lecturer_id>/', views.view_timetable, name='view_timetable'),
    # ADD TIMETABLE URL
    path('add_timetable_for_lecturer/<int:lecturer_id>/', views.add_timetable, name='add_timetable_for_lecturer'),
    # ADD TIMETABLE URL
    path('add-timetable/<int:lecturer_id>/', views.add_timetable, name='add_timetable'),
    # EDIT TIMETABLE URL
    path('timetable/edit/<int:timetable_id>/', views.edit_timetable, name='edit_timetable'),
    # DELETE TIMETABLE URL
    path('timetable/delete/<int:timetable_id>/', views.delete_timetable, name='delete_timetable'),
    # DELETE LECTURER URL
    path('delete-lecturer/<int:lecturer_id>/', views.delete_lecturer, name='delete_lecturer'),
    # EDIT LECTURER URL
    path('edit-lecturer/<int:lecturer_id>/', views.edit_lecturer, name='edit_lecturer'),
    # ALL ADMINS URL
    path('all-admins/', views.all_admins, name='all_admins'),
    # ALL ADMINS URL
    path('all-admins/', views.all_admins, name='all_admins'),
   
 
    # TEST URL
    path('tailwind-test/', views.tailwind_test, name='tailwind_test'),
    # DEPARTMENT URL
    path('departments-courses/', views.departments_courses, name='departments_courses'),
    path('add-department/', views.add_department, name='add_department'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),

    # Add these URL patterns to your existing urls.py file

    path('update-admin/<int:admin_id>/', views.update_admin, name='update_admin'),
    path('delete-admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
]
