from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Car(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image_url = models.TextField(default="No Image")
    category = models.CharField(max_length=64, default="other")
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_auctions")    # who created this listing
    active = models.BooleanField(default=True)    # state of the listing: active or closed, to determine the highest bidder

    def __str__(self) :
        return f"Title: {self.title}, Desc: {self.description}, id: {self.id}"
    
class Comment(models.Model) :
    # the user that made the comment
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    # on which car listing was this comment made
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car", null=True)

    # content of the comment
    content = models.CharField(max_length=255)


class WatchList(models.Model) :
    # which car is added to the watchlist
    car_listing = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_listing")

    # whose watchlist does this belong to
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

class Bid(models.Model):
    # who place the bid, this tracks the current highest bidder for this listing
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    # the listing that the bid was placed on
    car_listing = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="listing")