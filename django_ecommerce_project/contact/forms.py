from django.forms import ModelForm
from .models import ContactForM
from django import forms

class ContactView(ModelForm):
    message=forms.CharField(widget=forms.Textarea)
    
    class Meta:
        fields = ['name', 'email','topic', 'message']
        model = ContactForM