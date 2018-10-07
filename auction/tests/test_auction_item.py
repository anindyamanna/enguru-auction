from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mixer.backend.django import mixer

from auction.models import AuctionItem


class TestAuctionItem(TestCase):

    def test_without_any_query_params(self):
        """
        Testing list Api endpoint to return upcoming auction items correctly.
        """
        mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(hours=1),
                    end_time=timezone.now() + timedelta(days=1))  # Ongoing item
        mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(days=1),
                    end_time=timezone.now() - timedelta(hours=1))  # Past item
        mixer.blend(AuctionItem, start_time=timezone.now() + timedelta(hours=1),
                    end_time=timezone.now() + timedelta(days=1))  # Upcoming item

        resp = self.client.get(reverse('auction:list-auction-items')).json()

        self.assertEqual(len(resp), 3)

    def test_upcoming_dates(self):
        """
        Testing list Api endpoint to return upcoming auction items correctly.
        """
        mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(hours=1),
                    end_time=timezone.now() + timedelta(days=1))  # Ongoing item
        mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(days=1),
                    end_time=timezone.now() - timedelta(hours=1))  # Past item
        upcoming_item = mixer.blend(AuctionItem, start_time=timezone.now() + timedelta(hours=1),
                                    end_time=timezone.now() + timedelta(days=1))  # Upcoming item

        resp = self.client.get(reverse('auction:list-auction-items') + "?upcoming=true").json()

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0].get("item_name"), upcoming_item.item_name)

    def test_previous_dates(self):
        """
        Testing list Api endpoint to return previous auction items correctly.
        """
        mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(hours=1),
                    end_time=timezone.now() + timedelta(days=1))  # Ongoing item
        prev_item = mixer.blend(AuctionItem, start_time=timezone.now() - timedelta(days=1),
                                end_time=timezone.now() - timedelta(hours=1))  # Past item
        mixer.blend(AuctionItem, start_time=timezone.now() + timedelta(hours=1),
                    end_time=timezone.now() + timedelta(days=1))  # Upcoming item

        resp = self.client.get(reverse('auction:list-auction-items') + "?previous=true").json()

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0].get("item_name"), prev_item.item_name)
