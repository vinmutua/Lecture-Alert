from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import datetime


class PasswordMixin:
    """
    A mixin to handle password hashing and verification.
    """
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Department(models.Model):
    name = models.CharField(max_length=100, default='Unknown Department')  # Add default value
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Make nullable

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, default='Unknown Course')  # Add default value
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)  # Make nullable
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


class Lecturer(models.Model, PasswordMixin):
    username = models.CharField(max_length=30, unique=True, default='default_lecturer')  # Add default value
    fullname = models.CharField(max_length=255, default='Unknown Lecturer')  # Add default value
    email = models.EmailField(unique=True, default='lecturer@example.com')  # Add default value
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=128, default='default_password')  # Add default value
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='lecturers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class Admin(models.Model, PasswordMixin):
    username = models.CharField(max_length=30, unique=True, default='default_username')  # Add default value
    fullname = models.CharField(max_length=255, default='Unknown Admin')  # Add default value
    email = models.EmailField(unique=True, default='admin@example.com')  # Add default value
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=128, default='default_password')  # Add default value
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class Timetable(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100, default='Unknown Venue')  # Add default value
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.lecturer.fullname} - {self.course.name} ({self.date})"

    def get_time_status(self):
        """Return the status of the lecture: upcoming, ongoing, or completed"""
        now = timezone.localtime()
        today = now.date()
        current_time = now.time()
        
        if self.date > today:
            return 'upcoming'
        elif self.date == today:
            if current_time < self.start_time:
                return 'upcoming'
            elif self.start_time <= current_time <= self.end_time:
                return 'ongoing'
            else:
                return 'completed'
        else:
            return 'completed'