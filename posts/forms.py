from django import forms
from .models import User
from .validators import validate_symbols
from django.core.exceptions import ValidationError



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'user_pic',
            'student_number',
            'major',
            'join_year',
            
        ]
        widgets = {
            'join_year': forms.Select
        }
