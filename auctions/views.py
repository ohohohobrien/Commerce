from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Categories, Comments, Bids, WatchList

# not finished yet
class NewListingForm(forms.Form):
    name = forms.CharField(max_length=64, label="Name", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}), max_length=1014, label="Description")
    image = forms.URLField(max_length=1024, required=False, widget=forms.URLInput(attrs={'class' : 'form-control'}))
    starting_price = forms.DecimalField(label="Starting Price", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    categories = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="None", required=False, widget=forms.Select(attrs={'class' : 'form-control'}))

class BiddingForm(forms.Form):
    bid = forms.DecimalField(label="New Bid Amount", max_digits=10, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class' : 'form-control'}))

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=1014, label="Comment")

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), required=True, empty_label=None, widget=forms.Select(attrs={'class' : 'form-control'}))

def index(request):
    auction = AuctionListing.objects.filter(active_listing=True) # this is just a code editor error - it's ok
    return render(request, "auctions/index.html", {
        "auction_items": auction,
    })

def listing(request, listing_id):

    listing = AuctionListing.objects.get(pk=listing_id)

    # Get the top bid for the item when page is loaded
    top_bid = Bids.objects.filter(auction_item=listing)
    top_bid = top_bid.last()
    top_bid_exists = False

    if top_bid:
        top_bid_exists = True
        print("Top bid exists.")
    else:
        top_bid = listing.price
        top_bid_exists = False
        print("Top bid does not exist.")
        print(top_bid)

    on_watchlist = False

    if request.user.is_authenticated:
        watchlist = WatchList.objects.filter(user=request.user,auction_item=listing_id)

        if watchlist: # if the item exists on the watchlist
            on_watchlist = True

        if request.method == "POST":

            form = BiddingForm(request.POST)
            
            if 'bid' in request.POST:
            
                if form.is_valid():
                    
                    if top_bid_exists:
                        previous_top_bid = float(top_bid.bid)
                    else:
                        previous_top_bid = float(listing.price)

                    new_bid = form.cleaned_data["bid"]
                    new_bid = float("{:.2f}".format(new_bid)) # force 2 decimal places

                    if new_bid > previous_top_bid:
                        print("New bid accepted at " + str(new_bid))
                        bid_to_record = Bids(bid=new_bid, user=request.user, auction_item=listing)
                        bid_to_record.save()
                        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
                    else:
                        print("Bid not accepted as " + str(new_bid) + " is not higher than current bid")

            if 'watchlist' in request.POST:
                print(request.POST)

                try:
                    watchlist_check = WatchList.objects.get(user=request.user, auction_item=listing)
                    print(watchlist_check)
                except:
                    watchlist = WatchList(user=request.user, auction_item=listing)
                    watchlist.save()
                    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))

                # if already exists
                watchlist_check.delete()
                return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
            
            if 'close_auction' in request.POST:
                print(request.POST)

                listing.active_listing = False

                if top_bid_exists:
                    listing.winner = top_bid.user
                else:
                    print("Closed with no winner.")
                listing.save()
                print(str(listing) + " listing status set to inactive.")
                return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))

    form = BiddingForm()

    # if GET request
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user,
        "on_watchlist": on_watchlist,
        "form": form,
        "current_bid": top_bid
    })

@login_required(login_url='/login')
def comment(request, listing_id):
    
    if request.method == "POST":
        
        form = CommentForm(request.POST)

        if form.is_valid():
            
            text = form.cleaned_data["comment"]
            listing = AuctionListing.objects.get(pk=listing_id)
            comment = Comments(comment=text, user=request.user, listing=listing)
            comment.save()

    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))

@login_required(login_url='/login')
def watchlist(request):

    watchlist = WatchList.objects.filter(user=request.user)
    listing = watchlist.select_related()
    
    return render(request, "auctions/watchlist.html", {
        "auction_items": listing
    })
    
@login_required(login_url='/login')
def create(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            starting_price = form.cleaned_data["starting_price"]
            category = form.cleaned_data["categories"]

            # Create the new object in the AuctionListing model
            new_listing = AuctionListing(title=name, description=description, price=starting_price, active_listing=True, created_by=request.user)
            if category:
                print(category)
                new_listing.category = category
            if image:
                print(image)
                new_listing.image = image    
            new_listing.save()
            print(new_listing)
            print("Added to database")

            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': new_listing.id}))
            
    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

def category_search(request):

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            
            category = form.cleaned_data["category"]
            search = Categories.objects.get(category_name=category)
            listings = AuctionListing.objects.filter(category=search, active_listing=True)
            print(listings)

            return render(request, "auctions/category-search.html", {
                "category": category,
                "auction_items": listings
            })

    return render(request, "auctions/category.html", {
        "form": CategoryForm()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #user = User(first_name=first_name, last_name=last_name)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
