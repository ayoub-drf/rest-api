from django.utils.text import _
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    name = models.CharField(max_length=60)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts") 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"pk": self.pk})
