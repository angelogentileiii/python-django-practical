from django.contrib import admin

from .models import Book, Author, Address, Country


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
    fields = ("title", "published_countries")
    readonly_fields = ("title", "published_countries")


class AuthorAdmin(admin.ModelAdmin):
    list_filter = (
        "first_name",
        "last_name",
    )

    inlines = [BookInline]

    list_display = ("__str__", "get_books")

    def get_books(self, obj):
        books = obj.books.all()  # Access the related books via the related name
        return ", ".join([f"{book.title}" for book in books])

    get_books.short_description = "Books"


class AddressAdmin(admin.ModelAdmin):
    list_filter = ("city",)
    list_display = (
        "street",
        "city",
        "post_code",
        "get_author",
    )

    def get_author(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}"
        else:
            return "No Author"

    # Optional: Set the column name in the admin list view
    get_author.short_description = "Author"


class CountryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_books")

    def get_books(self, obj):
        books = obj.books.all()  # Access the related books via the related name
        return ", ".join([f"{book.title} by {book.author}" for book in books])

    # Optional: Set the column name in the admin list view
    get_books.short_description = "Books"


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Country, CountryAdmin)
