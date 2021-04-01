from django.contrib import admin
from .models import User, AuctionListing, Categories, Comments, Bids, WatchList

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "active_listing")

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing, AuctionAdmin)
admin.site.register(Categories)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(WatchList)