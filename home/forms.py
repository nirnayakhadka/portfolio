from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': ' ',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': ' ',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': ' ',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'placeholder': ' ',
                'required': True,
                'rows': 5
            }),
        }