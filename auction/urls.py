from django.urls import path
from rest_framework.authtoken import views

from auction.views import ListAuctionItems

app_name = 'auction'
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('list-auction-items/', ListAuctionItems.as_view(), name='list-auction-items'),
]
