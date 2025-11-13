from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile, CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.

admin.site.register(Author)
admin.site.register(Book)   
admin.site.register(Library)
admin.site.register(Librarian)
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