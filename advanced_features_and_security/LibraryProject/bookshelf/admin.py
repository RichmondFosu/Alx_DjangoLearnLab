from django.contrib import admin
from .models import Book, CustomUser,  UserProfile
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(Book)
admin.site.register(UserProfile)

class CustomUserAdmin(UserAdmin):
    # fields displayed in user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')

    # fields when editing user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register custom user model with admin
admin.site.register(CustomUser, CustomUserAdmin)


