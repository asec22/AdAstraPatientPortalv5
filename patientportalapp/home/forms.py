from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        labels={
            "name":"Name",
            "email":"Email",
            "message":"Message",
        }
        fields = ['name', 'email', 'message']