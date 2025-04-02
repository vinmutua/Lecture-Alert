from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Admin, Lecturer, Course

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
        }),
        required=False,  # Not required for updates
        help_text='Leave blank to keep current password'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
        }),
        required=False  # Not required for updates
    )

    class Meta:
        model = Admin
        fields = ['fullname', 'username', 'email', 'phone']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter full name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter phone number'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username exists but exclude current instance
        if Admin.objects.filter(username=username).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('This username is already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email exists but exclude current instance
        if Admin.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('This email is already registered')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password:
            # Validate password only if provided
            validate_password(password)
            if password != confirm_password:
                raise forms.ValidationError({
                    'confirm_password': 'Passwords do not match'
                })

        return cleaned_data


class LecturerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Enter password'
        }),
        required=True,
        help_text='Minimum 8 characters'
    )

    class Meta:
        model = Lecturer
        fields = ['fullname', 'username', 'email', 'phone', 'department', 'courses']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter full name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'placeholder': 'Enter phone number'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show errors if form has been submitted
        if not self.is_bound:  # Form hasn't been submitted
            self._errors = {}
            for field in self.fields.values():
                field.widget.attrs['required'] = False

    def clean(self):
        if not self.is_bound:  # Skip validation if form hasn't been submitted
            return self.cleaned_data
        cleaned_data = super().clean()
        if 'password' in cleaned_data:
            try:
                validate_password(cleaned_data['password'])
            except forms.ValidationError as e:
                self.add_error('password', e)
        return cleaned_data


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class LecturerLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class LecturerUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': 'Leave blank to keep current password'
        }),
        required=False,
        help_text='Leave blank to keep current password'
    )

    class Meta:
        model = Lecturer
        fields = ['fullname', 'username', 'email', 'phone']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            })
        }


class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ['department', 'courses']
        widgets = {
            'department': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'courses': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.department:
            self.fields['courses'].queryset = Course.objects.filter(
                department=self.instance.department
            )
        # Change courses field to single select instead of multiple
        self.fields['courses'].required = True
        self.fields['courses'].widget = forms.Select(
            attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm'}
        )