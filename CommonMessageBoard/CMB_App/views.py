from django.shortcuts import HttpResponse, render, HttpResponseRedirect, redirect
from random import shuffle
from datetime import datetime, timedelta
from django.contrib.humanize.templatetags import humanize

from .models import User, Message

# Index View
def index(request):
    if request.method == "POST":
        # If request method was POST, try verifying credentials

        # Get username from request data
        username = request.POST.get("username", None)
        
        # If username was not provided, redirect to homepage
        if not username:
            return redirect("index")

        # Try checking if user exists
        # If not, redirect to homepage
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect("index")

        # Check if user classified all incorrect secret codes
        # If not, redirect to homepage
        for value in user.incorrect_passwords:
            if request.POST.get(value, None) != "unselected":
                return redirect("index")
        
        # Check if user classified all correct secret codes
        # If not, redirect to homepage
        for value in user.correct_passwords:
            if request.POST.get(value, None) != "selected":
                return redirect("index")

        # If credentials were verified, store necessary user data in session data
        request.session["logged_in"] = True
        request.session["username"] = username

        # Redirect user to homepage
        return redirect("index")
    elif request.method != "GET":
        # If request is not GET or POST, redirect to homepage
        return redirect("index")
    elif request.session.get("logged_in", False):
        # If logged in, display message board

        # Filter all messages from past 24 hours
        # Filter help from https://stackoverflow.com/questions/27770837/django-return-count-when-date-stored-last-24-hours
        messages = Message.objects.filter(created__gte=datetime.now() - timedelta(days=1))

        # Display homepage with all recent messages
        return render(request, "CMB_App/index.html", {
            "messages": messages
        })
    else:
        # If it is a GET request with a logged out user, display login page
        return render(request, "CMB_App/login.html")

# Secret Code Selection View
def password_select(request):
    # If request method is not POST or user is logged in, redirect to homepage
    if request.method != "POST" or request.session.get("logged_in", False):
        return redirect("index")
    
    # Get username from request data
    username = request.POST.get("username", None)

    # If username was not provided, redirect to homepage
    if not username:
        return redirect("index")

    # Try checking if user exists
    # If not, redirect to homepage
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect("index")
    
    # If user exists, combine the list of all their codes (secret and fake) and shuffle them randomly for security purposes
    options = user.correct_passwords + user.incorrect_passwords
    shuffle(options)
    
    # Display secret code selection screen
    return render(request, "CMB_App/password_select.html", {
        "options": options,
        "username": username
    })

# Create Account View
def create_account(request):
    # If user is logged in, redirect to homepage
    if request.session.get("logged_in", False):
        return redirect("index")
    
    # If request method is GET, display account creation page
    if request.method == "GET":
        return render(request, "CMB_App/create_account.html", {
            "counter": range(1, 21)
        })
    
    # If request method is not GET or POST, redirect to homepage
    if request.method != "POST":
        return redirect("index")
    
    # Get username from request data
    username = request.POST.get("username", None)

    # If no username was provided, redirect to account creation page
    if not username:
        return redirect("create-account")
    
    # Create a value to check if user exists already
    userExists = False
    
    # Try finding if a user with given username already exists and update value from above
    try:
        user = User.objects.get(username=username)
        userExists = True
    except User.DoesNotExist:
        userExists = False
    
    # If user already exists, redirect to account creation page
    if userExists:
        return redirect("create-account")
    
    # Create empty lists representing correct and incorrect secret codes
    correct_passwords = []
    incorrect_passwords = []

    # Go through all 20 secret codes given and append them to the appropriate lists
    for i in range(1, 21):
        if request.POST.get(f"{i}_checked", None) == "checked":
            correct_passwords.append(request.POST.get(f"{i}", None))
        else:
            incorrect_passwords.append(request.POST.get(f"{i}", None))
    
    # If the length of the secret code lists are not correct, redirect to account creation page
    if len(correct_passwords) != 5 or len(incorrect_passwords) != 15:
        return redirect("create-account")
    
    # If user data is correct, create user
    User.objects.create(username=username, correct_passwords=correct_passwords, incorrect_passwords=incorrect_passwords)

    # Redirect to homepage
    return redirect("index")

# Post View
def post(request):
    # If method used is not POST, redirect to homepage
    if request.method != "POST":
        return redirect("index")
    
    # Get title and message of post from request data
    title = request.POST.get("title", None)
    message = request.POST.get("message", None)

    # If all necessary information is not provided, redirect to homepage
    if not title or not message:
        return redirect("index")

    # Get the current user object
    user = User.objects.get(username=request.session["username"])

    # Create the message object
    Message.objects.create(title=title, message=message, user=user)

    # Redirect to homepage
    return redirect("index")

# Logout View
def logout(request):
    # Remove the stored session values associated with the logged in user
    request.session["logged_in"] = False
    request.session["username"] = None

    # Redirect to homepage
    return redirect("index")