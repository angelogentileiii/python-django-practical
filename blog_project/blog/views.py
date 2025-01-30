from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import ListView
from django.views import View

from .models import Post
from .forms import CommentForm

# Create your views here.

# def home_page(request):
#     # Django converts the method below into a single SQL query --> Optimized
#     #   - Negative indexes for slicing would not be supported
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": latest_posts})

class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set[:3]
    
# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/posts.html", {"all_posts": all_posts})

class AllPostsView(ListView):
    model = Post
    template_name = "blog/posts.html"
    context_object_name = "all_posts"
    ordering = ["-date"]


# def post_detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-detail.html", {"post": post, "post_tags": post.tags.all()})

class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            saved_for_later = post_id in stored_posts
        else:
            saved_for_later = False
        
        return saved_for_later

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
            }
        
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # Creates a new comment instance in the database --> Saving to variable allows us to manipulate data
            comment.post = post # Add the post data (relation) to the comment before saving to the database
            comment.save() # Finally save and instantiate the comment in the database

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
    
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }

        return render(request, "blog/post-detail.html", context)


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        context["comment_form"] = CommentForm()
        return context

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if not stored_posts:
            context["posts"] = []
            context["has_posts"] = None
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if not stored_posts:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")