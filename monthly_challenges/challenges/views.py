from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# Monthly challenge object used to afford long if or match/case statement
monthly_challenges = {
    "january": "This is January and works!",
    "february": "Welcome to February!",
    "march": "Oh wow! Already March!",
    "april": "Oh wow! Already April!",
    "may": "Oh wow! Already May!",
    "june": "Oh wow! Already June!",
    "july": "Oh wow! Already July!",
    "august": "Oh wow! Already August!",
    "september": "Oh wow! Already September!",
    "october": "Oh wow! Already October!",
    "november": "Oh wow! Already November!",
    "december": "Oh wow! Already December!",
}


# EVERY VIEW IS A STANDALONE FUNCTION --> CAN BE SPLIT AMONGST MULTIPLE FILES
# def january(request):
#     print("Request: ", request)
#     return HttpResponse("<h1>This works!</h1>")


# def february(request):
#     return HttpResponse("<h1>Welcome to February!</h1>")


def index(request):
    months = list(monthly_challenges.keys())
    links = []
    for month in months:
        links.append(
            f"<a href={reverse("month-challenge", args=[month])}>{month.capitalize()}</a>"
        )
    print(links)
    response_data = "</br>".join(links)
    return HttpResponse(response_data)


# The second argument must match the concrete value that is passed to the url path within '<>'
def monthly_challenge(request, month):
    try:
        challenge_text = monthly_challenges[month.lower()]
        response_data = f"<h1>{challenge_text}</h1>"
        return HttpResponse(response_data)
    except:
        return HttpResponseNotFound("<h1>This month is not supported</h1>")


def monthly_challenge_by_number(request, month):
    months = list(monthly_challenges.keys())

    if month > len(months):
        return HttpResponseNotFound("<h1>Invalid month entered</h1>")

    redirect_month = months[month - 1]

    # The reverse function helps create a dynamic path to the proper view by utilizing the name argument of that path
    # Much better than hard coding a path to redirect to --> Prevents future errors if the overall path changes
    redirect_path = reverse("month-challenge", args=[redirect_month])
    return HttpResponseRedirect(redirect_path)
