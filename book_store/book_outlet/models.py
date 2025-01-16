from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


# Django will create a 'books' table in the database --> Lowercase and Pluralize classname
#   - Also will handle the primary key/autoincrement id
class Book(models.Model):
    # Import the Field Reference Types from the models import --> Check docs for types available
    #   - Arguments can either be required or not by the field being used
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # null=True allows NULL value in the column of the database --> blank=True allows value to be empty (different han having a NULL value)
    #   - blank=True is more used for values that are not received --> As in from a form that leaves an area empty
    #   - An empty string for CharField or TextFields should usually be an empty string --> Not the NULL value
    author = models.CharField(null=True, max_length=100)
    is_bestselling = models.BooleanField(default=False)

    # SlugField ensures it is a string in form 'word-word-23-word'
    # db_index --> This item will be used frequently for searching the database
    #   - The database more efficiently stores the data for this reason --> Speeds up search performance (But decreases perfomance on adding to the database)
    #   - Should only be used for values that are used for querying frequently
    # blank=True --> Also has implications in the admin site, means we do not need it to have the input filled in
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def __str__(self):
        return f"{self.title} ({self.rating})"

    # Overwrite the built in save method with some custom logic
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)

    #     Use super to ensure that the original save method is called and anything passed to the outer function is passed to the original save function
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book_detail", args=[self.slug])
