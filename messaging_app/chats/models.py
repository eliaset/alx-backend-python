from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # <-- new related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # <-- new related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.username} ({self.role})"
