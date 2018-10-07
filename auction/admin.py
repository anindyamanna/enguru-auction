from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auction.models import CustomUser, AuctionItem, Bid


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets[:2] + (
        (None, {'fields': ("full_name",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AuctionItem)
admin.site.register(Bid)
