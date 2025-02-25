from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home-page"),
    path("posts", views.posts, name="posts-page"),
    path(
        "posts/<slug:slug>", views.post_detail, name="post-detail-page"
    ),  # slug transformer (slug:) looks for text with characters or numbers and dashs "my-blog-post"
]
