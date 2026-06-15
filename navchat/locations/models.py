from django.conf import settings
from django.db import models


class UserLocation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='location',
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_sharing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = 'sharing' if self.is_sharing else 'hidden'
        return f'{self.user.username} ({status})'
