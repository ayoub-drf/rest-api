from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
