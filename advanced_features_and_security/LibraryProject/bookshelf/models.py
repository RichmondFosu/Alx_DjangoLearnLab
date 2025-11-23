from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# ================= CUSTOM USER MANAGER =================
class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    Handles user creation and superuser creation.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, password, **extra_fields)


# ================= CUSTOM USER MODEL =================
class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Added fields: date_of_birth, profile_photo
    """

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    # Connect the custom manager
    objects = CustomUserManager()

    # REQUIRED_FIELDS ensures superuser creation asks for email
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


# ================= USER PROFILE =================
class UserProfile(models.Model):
    """
    Extended profile for CustomUser with role-based access.
    Roles:
    - Admin: full access
    - Librarian: manage books
    - Member: read-only
    """

    ROLE_CHOICES = (
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ================= SIGNALS =================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new CustomUser is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile when the CustomUser is saved.
    """
    if hasattr(instance, "profile"):
        instance.profile.save()


# ================= BOOK MODEL (with permissions) =================
class Book(models.Model):
    """
    Simple Book model with custom permissions.
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.DateField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_view_book", "Can view book"),
            ("can_create_book", "Can create book"),
            ("can_edit_book", "Can edit book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author} ({self.published_year})"
