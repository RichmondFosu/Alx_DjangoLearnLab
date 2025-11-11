from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author.name}'
    
    class Meta:
        """
        Define custom permissions for Book model.
        
        Custom Permissions:
        - can_add_book: Permission to add new books
        - can_change_book: Permission to edit existing books
        - can_delete_book: Permission to delete books
        """
        permissions = (
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        )

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} at {self.library.name}'


# ============ USER PROFILE MODEL WITH ROLES ============

class UserProfile(models.Model):
    """
    Extended user profile with role-based access control.
    
    Roles:
    - Admin: Full access to all features
    - Librarian: Can manage library and books
    - Member: Regular user with read-only access
    """
    
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


# ============ DJANGO SIGNALS FOR AUTO PROFILE CREATION ============

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a UserProfile when a new User is created.
    
    This ensures every user automatically gets a profile with the default 'Member' role.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to automatically save the UserProfile when a User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()