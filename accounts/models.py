import uuid
from django.contrib.auth.models     import AbstractUser
from django.core.validators         import MaxValueValidator, MinValueValidator
from django.db                      import models


class CustomUser(AbstractUser):
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
