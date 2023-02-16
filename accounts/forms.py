from django import forms

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    #re_type_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'date_of_birth',
            'email', 'username',
        ]

    def clean_email(self):
        try:
            obj = CustomUser.objects.get(email=self.cleaned_data.get('email') or None)
        except:
            obj = None
        if obj:
            raise forms.ValidationError("user with this email already exists")
        return self.cleaned_data.get('email')

    #def clean_password(self):
    #    if self.cleaned_data.get('password') != self.cleaned_data.get('re_type_password'):
    #        print(self.cleaned_data)
    #        raise forms.ValidationError("password doesn't match")
    #    return self.password
        