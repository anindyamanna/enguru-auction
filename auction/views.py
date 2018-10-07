import coreapi
import coreschema
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView

from auction.models import AuctionItem
from auction.serializers import AuctionItemSerializer, AuctionItemDetailsSoldSerializer, BidSerializer


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


class AuctionItemDetails(APIView):
    """

    API to list details of an item. If the item is already auctioned, it will give the details of buyer and the
    amount. If the item is currently in auction, it will list the highest bid amount

    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            name="item_id",
            required=True,
            location="path",
            schema=coreschema.Integer(description="Id of the Auction item."),
        ),
    ])

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(AuctionItem, id=self.kwargs["item_id"])
        if item.end_time < timezone.now():
            resp = AuctionItemDetailsSoldSerializer(item).data
            resp.update({"already_auctioned": True})
            return Response(resp)
        else:
            resp = {
                "amount": item.bid_set.order_by('-amount')[0].amount if item.bid_set.exists() else item.starting_amount}
            resp.update({"already_auctioned": False})
            return Response(resp)


class ListBids(ListAPIView):
    """

    View all bids submitted by an authenticated user.

    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = BidSerializer
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
    ])

    def get_queryset(self):
        queryset = self.request.user.bid_set.all()
        page = int(self.request.query_params.get('page', 0))
        items_per_page = int(self.request.query_params.get('items_per_page', 10))
        queryset = queryset[page * items_per_page: (page + 1) * items_per_page]
        return queryset


class SubmitBid(APIView):
    """

    Submit new Bid.

    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post", ]
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            name="item_id",
            required=True,
            location="form",
            schema=coreschema.Integer(description="Id of the Auction item."),
        ),
        coreapi.Field(
            name="amount",
            required=True,
            location="form",
            schema=coreschema.Integer(description="Amount"),
        ),
    ])

    def post(self, request, *args, **kwargs):
        amount = self.request.data.get("amount")
        item_id = self.request.data.get("item_id")
        if amount and item_id:
            try:
                item = AuctionItem.objects.get(id=item_id, running=True)
            except AuctionItem.DoesNotExist:
                return Response({'Error': "Auction Item is not up for bidding."})
            bid = self.request.user.bid_set.create(amount=amount, item=item)
            return Response(BidSerializer(bid).data)
        return Response({'Error': "Error creating Bid"})
