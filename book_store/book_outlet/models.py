from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


# Django will create a 'books' table in the database --> Lowercase and Pluralize classname
#   - Also will handle the primary key/autoincrement id


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Address(models.Model):
    street = models.CharField(max_length=80)
    post_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Address Entries"

    def __str__(self):
        return f"{self.street}, {self.city} {self.post_code}"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_books(self):
        return self.books.all()


class Book(models.Model):
    # Import the Field Reference Types from the models import --> Check docs for types available
    #   - Arguments can either be required or not by the field being used
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # Create a relationship to the Author class --> Foreign key
    #   - on_delete=models.CASCADE means that we will delete any books if the author is deleted
    # null=True allows NULL value in the column of the database --> blank=True allows value to be empty (different han having a NULL value)
    #   - blank=True is more used for values that are not received --> As in from a form that leaves an area empty
    #   - An empty string for CharField or TextFields should usually be an empty string --> Not the NULL value
    # This is a One-To-Many relationship using the ForeignKey model field and the Author class as the key
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books"
    )
    is_bestselling = models.BooleanField(default=False)

    # SlugField ensures it is a string in form 'word-word-23-word'
    # db_index --> This item will be used frequently for searching the database
    #   - The database more efficiently stores the data for this reason --> Speeds up search performance (But decreases perfomance on adding to the database)
    #   - Should only be used for values that are used for querying frequently
    # blank=True --> Also has implications in the admin site, means we do not need it to have the input filled in
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    published_countries = models.ManyToManyField(Country, related_name="books")

    def __str__(self):
        return f"{self.title} ({self.rating})"

    # Overwrite the built in save method with some custom logic
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)

    #     Use super to ensure that the original save method is called and anything passed to the outer function is passed to the original save function
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book_detail", args=[self.slug])
