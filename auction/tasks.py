from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from auction.models import AuctionItem


@shared_task()
def start_auction(auction_item_id):
    auction_item = AuctionItem.objects.get(id=auction_item_id)
    if not auction_item.running and not auction_item.once_auctioned:
        auction_item.running = True
        auction_item.save()
        end_auction.apply_async(args=[auction_item_id, ], eta=auction_item.end_time)


@shared_task()
def end_auction(auction_item_id):
    auction_item = AuctionItem.objects.get(id=auction_item_id)
    auction_item.running = False
    auction_item.once_auctioned = True
    sold_to = auction_item.bid_set.order_by('-amount')[0].user if auction_item.bid_set.exists() else None
    if sold_to:
        auction_item.winner = sold_to
        # send_mail(
        #     'Congratulations! You Won.',
        #     'You won {0} for amount {1}'.format(auction_item.item_name,
        #                                         sold_to.bid_set.filter(item=auction_item).order_by('-amount')[0]),
        #     'from@example.com',
        #     [sold_to.email, ],
        #     fail_silently=False,
        # )
    auction_item.save()
