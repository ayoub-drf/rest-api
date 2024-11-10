from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=100)
    external_website = models.URLField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Liker: {self.liker.username} Post ID : {self.post.id}"
    
    
    # def get_absolute_url(self, request=None):
    #     return reverse("retrieve-like", kwargs={"pk": self.pk})
    

class Monitor(models.Model):
    STATUS = [
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
    ]
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS)

    def __str__(self):
        return f"{self.name}"
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(null=True)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def name_in_uppercase(self):
        return f"{self.name.upper()}"

class Book(models.Model):
    id = models.BigAutoField(auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name='ID'
                        )
    name = models.CharField(max_length=100)
    published = models.DateField(auto_created=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.id}'
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.title} - {self.id}'
    
class Customer(models.Model):
    product = models.ManyToManyField(Product, related_name='products')
    uuid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.id}'
    

class Library(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
    

class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.player_name}'