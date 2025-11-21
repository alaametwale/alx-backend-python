<<<<<<< HEAD
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ============================
# Custom User Model
# ============================
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password_hash = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    username = None  # Disable username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


# ============================
# Conversation Model
# ============================
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)


# ============================
# Message Model
# ============================
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
=======
from django.db import models
from django.contrib.auth.models import AbstractUser

# Define the CustomUser model by inheriting from AbstractUser
# This allows us to use Django's built-in authentication features
# while giving us the flexibility to add custom fields later.
class CustomUser(AbstractUser):
    """
    A custom user model based on Django's AbstractUser.
    We can add custom fields specific to a messaging app here if needed,
    but for now, it serves to fulfill the requirement for a custom user model.
    """
    # Example of adding a custom field (optional for now, but good practice):
    # bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        """Returns the username as the string representation."""
        return self.username

    class Meta:
        """Metadata for the model."""
        verbose_name = "User"
        verbose_name_plural = "Users"
>>>>>>> 3a649449a61a17ea5d3214c20863e67fb301673f
