from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    class Meta:
        db_table = 'accounts_admin'



class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, related_name='lecturer_timetables')
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=100)

    class Meta:
        db_table = 'accounts_timetable'

    def __str__(self):
        return f"{self.course} on {self.date} at {self.start_time}"

class Lecturer(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    courses = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    class Meta:
        db_table = 'accounts_lecturer'
