from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CustomReporterRecord(models.Model):
    time_raised = models.DateTimeField(default=timezone.now, editable=False)
    reference = models.CharField(unique=True, max_length=20)
    description = models.TextField()


class Book(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField()


class Event(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return f"{self.name} at {self.location} on {self.date}"
