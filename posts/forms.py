from django import forms
from .models import User
from .validators import validate_symbols
from django.core.exceptions import ValidationError


class ProfileForm(forms.ModelForm): # 개인정보 추가 
    class Meta:
        model = User
        fields = (
            'name',
            'user_pic',
            'student_number',
            'major',
            'join_year',
            
        )
        widgets = {
            'join_year': forms.Select
        }

# class CustomUserCreationForm(UserCreationForm):
#     secret_number = forms.CharField(max_length=5, required=True)

#     class Meta:
#         model = User
#         fields = ['email', 'password1', 'password2', 'secret_number']

#     def clean_secret_number(self):
#         secret_number = self.cleaned_data.get('secret_number')
#         if secret_number != "01010":
#             raise forms.ValidationError("Invalid secret number.")
#         return secret_number
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("이미 사용 중인 이메일입니다.")
#         return email
#  #   def clean_email(self):
#   #      email = self.cleaned_data.get('email')
#    #     return email 
#     # 나중에 이메일 유효성 검사할때 

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    secret_number = forms.CharField(max_length=5, required=True)

    class Meta:
        model = User
        fields = ('email', 'secret_number')

    def clean(self):
        cleaned_data = super().clean()
        secret_number = cleaned_data.get('secret_number')
        if secret_number != "01010":
            raise forms.ValidationError("Invalid secret number.")

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user    
