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