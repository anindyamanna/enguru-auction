from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views
from django.contrib.auth.decorators import login_required

from auction.views import ListAuctionItems, AuctionItemDetails, ListBids, SubmitBid

router = routers.DefaultRouter()
app_name = 'auction'
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('auction-items/<int:item_id>', AuctionItemDetails.as_view(), name='auction-item-details'),
    path('auction-items/', ListAuctionItems.as_view(), name='list-auction-items'),
    path('list-bids/', login_required(ListBids.as_view()), name='list-bids'),
    path('submit-bid/', login_required(SubmitBid.as_view()), name='submit-bid'),

]
urlpatterns += router.urls
