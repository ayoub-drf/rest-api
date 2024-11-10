from django.contrib import admin

from .models import (
    Father,
    Child,
    Product
)

admin.site.register(Father)
admin.site.register(Product)