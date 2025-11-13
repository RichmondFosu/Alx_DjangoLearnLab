from django.contrib import admin
from .models import Author, Book, Library, Librarian
from django.contrib.auth.admin import UserAdmin


# Register your models here.

admin.site.register(Author)
admin.site.register(Book)   
admin.site.register(Library)
admin.site.register(Librarian)

