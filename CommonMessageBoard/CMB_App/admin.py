from django.contrib import admin

from .models import User, Message

# Register both created models for use in admin interface
admin.site.register(User)
admin.site.register(Message)