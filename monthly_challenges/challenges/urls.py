from django.urls import path
from . import views

# Configure a URL configuration --> Here it is only within the challenges app
urlpatterns = [
    # path("january", views.january),
    # path("february", views.february),
    # --------------------------------------
    path("", views.index, name="index"),
    # Placeholder within Django '<>' --> We don't care about the concrete value or want it to be dynamic
    # Can utlizie the type condition below to interpret the dynamic segment as an int or a string
    path("<int:month>", views.monthly_challenge_by_number),
    # Utilize the third argument (name) to set a path to be used for redirection from another view
    # Great to use for redirection rather than hard coding a path within the view
    path("<str:month>", views.monthly_challenge, name="month-challenge"),
]
