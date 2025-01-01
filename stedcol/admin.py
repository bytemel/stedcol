from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, MentorProfile, Course, MentorshipRequest, Instructor

# Register CustomUser with the admin interface
class CustomUserAdmin(UserAdmin):
       model = CustomUser
       list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
       list_filter = ['role', 'is_staff', 'is_active']
       search_fields = ['username', 'email']
       ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MentorProfile)
admin.site.register(Course)
admin.site.register(MentorshipRequest)
admin.site.register(Instructor)