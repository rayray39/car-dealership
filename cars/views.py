from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Car, Comment, WatchList, Bid


# Create your views here.

def index(request):
    # index page that shows all the active car listings
    return render(request, "cars/index.html", {
        "car_listings" : Car.objects.filter(active=True),
        "h2_title" : "Active Listings"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]    # get user name from form, input by user
        password = request.POST["password"]    # get password from form, input by user
        user = authenticate(request, username=username, password=password)  # log the user in using the credentials

        # Check if authentication successful
        if user is not None:
            # log the user in and bring the user back to the index url
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # user not able to authenticate
            return render(request, "cars/log_in.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cars/log_in.html")


def logout_view(request):
    # log current user out, and redirect to the index url
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # new user is trying to register by filling up HTML form
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "cars/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)  # create new user object
            user.save()
        except IntegrityError:
            return render(request, "cars/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        # if the user is just trying to get the page
        return render(request, "cars/register.html")

def create_new_listing(request) :
    # only authenticated users can create new listing
    if request.method == "POST" and request.user.is_authenticated :
        # user is submitting the form and trying to create a new car listing
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        owner = request.user
        new_car = Car.objects.create(title=title, description=description, price=price, image_url=image_url, category=category, owner=owner)
        # new_car.save()
        return HttpResponseRedirect(reverse("index"))   # once new car is created, direct to index page to see it among others
    else :
        return render(request, "cars/create_new_listing.html")  # if the user is just trying to get the page
    
def car_listing(request, listing_id) :
    # get the detailed look into the car listing page
    car = Car.objects.get(id=listing_id)
    comments = Comment.objects.filter(car=car)  # get any comments that belongs to this car
    inside_watchlist = False    # check if this listing is already inside the watchlist or not
    congrats_msg = None
    if request.user.is_authenticated:
        watchlist = WatchList.objects.filter(user=request.user)  # get the watchlist listings of this user
        for watchlist_listing in watchlist:
            # check if this car listing is already inside this user's wastchlist
            if watchlist_listing.car_listing.id == listing_id:
                inside_watchlist = True
                break
        if not car.active and request.user == Bid.objects.get(car_listing=car).bidder :
            # if the car is already closed, check if current user is the highest bidder
            congrats_msg = "Congratulations! You have won this bid!"
    return render(request, "cars/car_listing.html", {
        "car" : car, 
        "comments" : comments,
        "inside_watchlist" : inside_watchlist, 
        "congrats_msg" : congrats_msg
    })

def place_bid(request, listing_id) :
    # ensure that only authenticated user can place a bid
    car = Car.objects.get(id=listing_id)
    if request.method == "POST" and request.user.is_authenticated :
        new_bid = request.POST["new_bid"]
        new_bid = int(new_bid)
        if new_bid > car.price :
            car.price = new_bid
            car.save()
            try :   # a previous bid was already made on this car listing
                bid = Bid.objects.get(car_listing=car)
                bid.bidder = request.user   # update the current highest bidder to be the current user
                bid.save()
            except ObjectDoesNotExist: # no bids have been made yet, so create one for this car listing
                Bid.objects.create(bidder=request.user, car_listing=car)
            messages.success(request, "Your bid has successfully been placed!")
        else : 
            messages.error(request, "Your bid must be higher than the current price!")
    return HttpResponseRedirect(reverse("car_listing", args=[listing_id]))


def make_comment(request, listing_id) :
    # add a comment into the comment section of this listing, only authenticated users can comment
    if request.method == "POST" and request.user.is_authenticated :
        content = request.POST["content"]
        owner = request.user    # who made the comment
        car = Car.objects.get(id=listing_id)    # the comment is made on which car
        comment = Comment(owner=owner, content=content, car=car)    # what is the content of the comment
        comment.save()
    return HttpResponseRedirect(reverse("car_listing", args=[listing_id]))


def categories(request) :
    # shows a page with all the categories
    return render(request, "cars/categories.html")

def category(request, selected_category) :
    # like the index page of all the cars under this category
    cars = Car.objects.filter(category=selected_category, active=True)
    return render(request, "cars/index.html", {
        "car_listings" : cars,
        "h2_title" : selected_category
    })


def add_to_watchlist(request, listing_id) :
    # add this particular car listing into this user's watchlist, listing_id = car's id
    if request.method == "POST" and request.user.is_authenticated :
        car_listing = Car.objects.get(id=listing_id)
        user = request.user
        watchlist = WatchList(car_listing=car_listing, user=user)
        if not WatchList.objects.filter(car_listing=car_listing, user=user).exists() :
            # additional check to ensure listings added into user's watchlist are not added twice
            watchlist.save()
    return HttpResponseRedirect(reverse("car_listing", args=[listing_id]))

def remove_from_watchlist(request, listing_id) :
    # remove this car listing from the user's watchlist, listing_id = car's id
    if request.method == "POST" and request.user.is_authenticated : # form is submitted to remove the listing
        car_listing = Car.objects.get(id=listing_id)
        watchlist_car = WatchList.objects.get(car_listing=car_listing, user=request.user)
        watchlist_car.delete()  # remove this listing from the watchlist
    return HttpResponseRedirect(reverse("car_listing", args=[listing_id]))

def watchlist(request) :
    # the index page for the watchlist of this user, get cars that are in this user's watchlist
    cars_in_watchlist = WatchList.objects.filter(user=request.user)  # among all the watchlist obj, get the ones belonging to this user
    cars_id = [car.car_listing.id for car in cars_in_watchlist]  # get the ids of the car_listings, inside of each watchlist obj
    car_listings = Car.objects.filter(pk__in=cars_id, active=True)
    return render(request, "cars/index.html", {
        "car_listings" : car_listings,
        "h2_title" : "WatchList"
    })


def close_listing(request, listing_id) :
    # allows owner to close a listing and making it inactive
    car = Car.objects.get(id=listing_id)
    if request.method == "POST" and request.user.is_authenticated :
        if request.user.id == car.owner.id and car.active == True :    # check if authenticated user is the owner
            car.active = False
            car.save()
            return render(request, "cars/index.html", {
                "car_listings" : Car.objects.filter(active=True), 
                "h2_title" : "Active Listings"
            })
    else :
        return render(request, "cars/index.html", {
            "car_listings" : Car.objects.filter(active=True),
            "h2_title" : "Active Listings"
        })
    
def closed_listings(request) :
    # an index page to show all the car listings that were closed by their owners (not active)
    closed_car_listings = Car.objects.filter(active=False)
    return render(request, "cars/index.html", {
        "car_listings" : closed_car_listings,
        "h2_title" : "Closed Listings"
    })
