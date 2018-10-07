from rest_framework.serializers import ModelSerializer

from auction.models import AuctionItem


class AuctionItemSerializer(ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = '__all__'

