from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Avg

from .models import Book


# Create your views here.
def index(request):
    # using "-title" would order the data in descending order
    all_books = Book.objects.all().order_by("title")

    total_books = all_books.count()
    avg_rating = all_books.aggregate(Avg("rating"))

    return render(
        request,
        "book_outlet/index.html",
        context={
            "books": all_books,
            "total_books": total_books,
            "average_rating": avg_rating,
        },
    )


def book_detail(request, slug: str):
    # try:
    #     book = Book.objects.get(pk=id)  # Can use pk to target the primary key value
    # except:
    #     raise Http404()

    # Django shortcut that equates to the above try/except block for a 404 error
    book = get_object_or_404(Book, slug=slug)

    return render(
        request,
        "book_outlet/book_detail.html",
        context={
            "title": book.title,
            "author": book.author,
            "rating": book.rating,
            "is_bestseller": book.is_bestselling,
        },
    )
