from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Categories(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active_listing = models.BooleanField(default=True)
    image = models.URLField(null=True, blank=True, max_length=1024, default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listings")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="auction_listings_winner")
    category = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE, related_name="auction_listings")

    def __str__(self):
        return f"{self.title} active: {self.active_listing}"

class Bids(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    time_posted = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_bids")
    auction_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,  related_name="placed_bids")

    def __str__(self):
        return f"Bid of ${self.bid} made by {self.user} on {self.auction_item.title}."

class Comments(models.Model):
    comment = models.CharField(max_length=1024)
    time_posted = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")   

    def __str__(self):
        return f"Comment made by {self.user} on {self.listing.title}."

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_lists")
    auction_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watch_lists")

    def __str__(self):
        return f"{self.user} is watching the auction item {self.auction_item}."