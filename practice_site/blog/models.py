from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email_address = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=250)
    content = models.TextField(validators=[MinLengthValidator(25)])
    date = models.DateField(auto_now=True)
    image_name = models.CharField(max_length=25, )
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} by {self.author}'
