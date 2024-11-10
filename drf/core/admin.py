from django.contrib import admin

# Register your models here.
from .models import UserProfile, Post, Like, Book, Author, Customer, Product, Library, HighScore
admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(HighScore)