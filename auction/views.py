import coreapi
import coreschema
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.schemas import AutoSchema

from auction.models import AuctionItem
from auction.serializers import AuctionItemSerializer


class ListAuctionItems(ListAPIView):
    """

    API to list all items on auction, upcoming auctions, previous auctions.

    """
    serializer_class = AuctionItemSerializer
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            name="page",
            required=False,
            location="query",
            schema=coreschema.Integer(description="Page to be retrieved. Defaults to 0"),
        ),
        coreapi.Field(
            "items_per_page",
            required=False,
            location="query",
            schema=coreschema.Integer(description="Number of items to be displayed per page. Defaults to 10")
        ),
        coreapi.Field(
            "upcoming",
            required=False,
            location="query",
            schema=coreschema.Boolean(
                description="Display only upcoming Auction Items. Takes boolean. Defaults to false")
        ),
        coreapi.Field(
            "previous",
            required=False,
            location="query",
            schema=coreschema.Boolean(
                description="Display only previous Auction Items. Takes boolean. Defaults to false")
        ),
    ])

    def get_queryset(self):
        queryset = AuctionItem.objects.all()
        page = self.request.query_params.get('page', 0)
        items_per_page = self.request.query_params.get('items_per_page', 10)
        upcoming = self.request.query_params.get('upcoming', False)
        previous = self.request.query_params.get('previous', False)
        if upcoming:
            queryset = queryset.filter(start_time__gt=timezone.now())
        if previous:
            queryset = queryset.filter(end_time__lt=timezone.now())
        queryset = queryset[page * items_per_page: (page + 1) * items_per_page]
        return queryset
