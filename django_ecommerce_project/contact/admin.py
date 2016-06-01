from django.contrib import admin
from .models import ContactForM

class ContactFormAdmin(admin.ModelAdmin):
    class Meta:
        model=ContactForM
        
admin.site.register(ContactForM,ContactFormAdmin)
    