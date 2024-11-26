from django.db import models


class Father(models.Model):
    email = models.EmailField(max_length=100, null=True)
    
    def __str__(self):
        return f"{self.email}"
    
class Child(models.Model):
    father = models.ForeignKey(Father, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    day = models.DateField(null=True)

    def __str__(self):
        return f"Child {self.name}"
    
class Product(models.Model):
    image = models.ImageField(upload_to="images")
    file = models.FileField(upload_to="media/files")