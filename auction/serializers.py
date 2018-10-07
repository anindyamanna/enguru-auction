from rest_framework.serializers import ModelSerializer, SerializerMethodField

from auction.models import AuctionItem, CustomUser, Bid


class AuctionItemSerializer(ModelSerializer):
    class Meta:
        model = AuctionItem
        fields = '__all__'


class AuctionItemDetailsSoldCustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name')


class AuctionItemDetailsSoldBidAmountSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ('amount',)


class BidSerializer(ModelSerializer):
    item = AuctionItemSerializer()

    class Meta:
        model = Bid
        fields = ('item', 'amount')
        depth = 1


class AuctionItemDetailsSoldSerializer(ModelSerializer):
    winner = AuctionItemDetailsSoldCustomUserSerializer()
    amount = SerializerMethodField()

    class Meta:
        model = AuctionItem
        fields = ('winner', 'amount')

    @staticmethod
    def get_amount(obj):
        if Bid.objects.filter(user=obj.winner, item=obj).exists():
            return AuctionItemDetailsSoldBidAmountSerializer(
                Bid.objects.filter(user=obj.winner, item=obj).order_by('-amount')[0]).data
        else:
            return ""
