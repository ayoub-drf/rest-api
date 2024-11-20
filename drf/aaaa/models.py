from django.db import models
from django.utils.text import slugify

class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.artist)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return "%d: %s" % (self.order, self.title)
    
    class Meta:
        unique_together = ["album", "order"]


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    publisher = models.OneToOneField(Publisher, related_name='book', on_delete=models.CASCADE)
    slug = models.SlugField(null=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
