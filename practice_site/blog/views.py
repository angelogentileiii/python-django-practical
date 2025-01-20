from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def home_page(request):
    # Django converts the method below into a single SQL query --> Optimized
    #   - Negative indexes for slicing would not be supported
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {"posts": latest_posts})


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/posts.html", {"all_posts": all_posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {"post": post, "post_tags": post.tags.all()})
