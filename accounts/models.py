import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Attributes:
        time_created (DateTimeField): Timestamp when the user was created.
        id (UUIDField): Primary key as UUID.
        age (SmallIntegerField): Age of the user (between 13 and 99, default 18).
        can_be_contacted (BooleanField): Indicates if the user can be contacted.
        can_data_be_shared (BooleanField): Indicates if user data can be shared.
    """
    time_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.SmallIntegerField(
        validators=[MinValueValidator(13), MaxValueValidator(99)],
        blank=True,
        null=False,
        default=18,
    )
    can_be_contacted = models.BooleanField(blank=False, null=False)
    can_data_be_shared = models.BooleanField(blank=False, null=False)
