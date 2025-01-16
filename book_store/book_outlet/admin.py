from django.contrib import admin

from .models import Book


# Register your models here.


# Class to alter the admin panel of the Django project for the class
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "author",
        "rating",
    )
    list_display = ("title", "author", "rating", "is_bestselling")


admin.site.register(Book, BookAdmin)
