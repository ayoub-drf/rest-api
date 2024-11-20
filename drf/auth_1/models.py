from django.db import models
from django.contrib.auth.models import User
from .utils import generateKey

class ApiKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.api_key = generateKey()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.api_key}"


