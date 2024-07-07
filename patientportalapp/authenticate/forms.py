from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group,User

class RegisterForm(UserCreationForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "groups", "username", "email", "password1", "password2"]