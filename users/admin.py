from django.contrib import admin
from .models import UserProfile,UserAccount

admin.site.register(UserProfile)
admin.site.register(UserAccount)
