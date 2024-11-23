from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=22.99)
    published_at = models.IntegerField()
    stock = models.IntegerField(default=2)

    categories = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, related_name="books")

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
