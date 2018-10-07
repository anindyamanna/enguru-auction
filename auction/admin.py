from django.contrib import admin

from auction.models import CustomUser, AuctionItem, Bids

admin.site.register(CustomUser)
admin.site.register(AuctionItem)
admin.site.register(Bids)
