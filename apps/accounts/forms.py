from django import forms
from .models import Admin, Lecturer

class UserLoginForm(forms.Form):
    username = forms.CharField()  # Changed back to username
    role = forms.ChoiceField(choices=[
        ('Lecturer', 'Lecturer'), 
        ('Admin', 'Admin')
    ])
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('Lecturer', 'Lecturer'), ('Admin', 'Admin')])

    class Meta:
        model = Admin  # Default to Admin model
        fields = ('email', 'username', 'fullname', 'phone')