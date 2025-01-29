from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView

from .forms import ReviewForm
from .models import Review

# Create your views here.

# Class Base View - FormView
#   - The FormView handles the get method out of the box
#   - We simply need to add the success_url for redirect on successful submission and a form_valid method
#       - Within this method, we determine what we accomplish with the submitted data
# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = "reviews/review.html"
#     success_url = "/thank-you"

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
    
# Class Based View - CreateView
#   - Will allow us to automatically create data in the database utilizing the submitted data
#   - There are also UpdateViews and DeleteViews which work in a similar manner by integrating with the database
class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"


# Class Base View - Basic
# class ReviewView(View):
#     # We can build class view methods that represent HTTP requests --> Slightly more understandable/cleaner
#     def get(self, request):
#         form = ReviewForm()

#         return render(request, "reviews/review.html", {"form": form})

#     def post(self, request):
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             print(form.cleaned_data)

#             # Because we are using a ModelForm, we can simply call save on the form to store into the inferred model table directly from the form
#             form.save()

#             return HttpResponseRedirect("/thank-you")

#         return render(request, "reviews/review.html", {"form": form})

# Standard Function Based View
# def review(request):
#     if request.method == "POST":
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             print(form.cleaned_data)

#             # Because we are using a ModelForm, we can simply call save on the form to store into the inferred model table directly from the form
#             form.save()

#             return HttpResponseRedirect("/thank-you")
#     else:
#         form = ReviewForm()

#     return render(request, "reviews/review.html", {"form": form})

class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This Works!"
        return context
    
# ListView is a more specialized TemplateView for displaying a list of data
class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    # Way to change the name of the data when it is exposed to the template
    context_object_name = "reviews"

    # Can limit or adjust our data queried from the DB
    # def get_queryset(self):
    #     base_query =  super().get_queryset()
    #     data = base_query.filter(rating__gt=3)
    #     return data

# DetailView is a more specialized TemplateView for displaying the details of a single piece of data
#   - Can find the item based on Primary Key or a Slug
#   - It will pull the slug or pk from the dynamic url automatically
# This detail view will pass the data to the template as a singular, lowercase version of the class name ("review" in this case) 
#   - We can also extract values in the template by using "object"
class ReviewDetailView(DetailView):
    template_name = "reviews/review_details.html"
    model = Review
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get("favorite_review") # Will not throw an error if the session data has not been set yet
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)
    