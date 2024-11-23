from django.db import models

class Product(models.Model):
    name = models.CharField(null=True, max_length=100, default="Product")

    def __str__(self):
        return f'{self.name}'
