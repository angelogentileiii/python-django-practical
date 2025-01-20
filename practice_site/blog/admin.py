from django.contrib import admin

from .models import Post, Author, Tag

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date", "get_tags")

    list_filter = ("author", "tags", "date")

    prepopulated_fields = {"slug": ("title",)}

    def get_tags(self, obj):
        tags = obj.tags.all()
        return ", ".join([tag.caption for tag in tags])
    
    get_tags.short_description = "Tags"
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_posts")

    list_filter = ("last_name",)

    def get_posts(self, obj):
        posts = obj.posts.all()
        return ", ".join([post.title for post in posts])
    
    get_posts.short_description = "Posts"

admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)