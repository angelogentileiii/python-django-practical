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
    date = models.DateField(auto_now=True, null=True)
    image = models.ImageField(upload_to="posts")
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} by {self.author}'
    
class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")