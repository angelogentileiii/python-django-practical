from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View

from .forms import ReviewForm

# Create your views here.

# Class Base View
class ReviewView(View):
    # We can build class view methods that represent HTTP requests --> Slightly more understandable/cleaner
    def get(self, request):
        form = ReviewForm()

        return render(request, "reviews/review.html", {"form": form})

    def post(self, request):
        form = ReviewForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            # Because we are using a ModelForm, we can simply call save on the form to store into the inferred model table directly from the form
            form.save()

            return HttpResponseRedirect("/thank-you")

        return render(request, "reviews/review.html", {"form": form})

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

def thank_you(request):
    return render(request, "reviews/thank_you.html")