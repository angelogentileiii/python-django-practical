from django.contrib import admin

from .models import Book, Author


# Register your models here.


# Class to alter the admin panel of the Django project for the class
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "author",
        "rating",
    )
    list_display = ("title", "author", "rating", "is_bestselling")


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ("title",)
    readonly_fields = ("title",)


class AuthorAdmin(admin.ModelAdmin):
    list_filter = (
        "first_name",
        "last_name",
    )
    inlines = [BookInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
