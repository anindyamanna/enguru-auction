from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extending the default User class to add custom fields.
    """
    full_name = models.CharField(max_length=256, null=True, blank=True, verbose_name="Full Name")

    def save(self, *args, **kwargs):
        """
        Overriding save method to set username automatically from email.
        """
        self.username = self.email
        super(CustomUser, self).save(*args, **kwargs)


class AuctionItem(models.Model):
    item_name = models.CharField(max_length=256)
    item_description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    running = models.BooleanField(default=False)
    once_auctioned = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(AuctionItem, self).save(force_insert, force_update, using, update_fields)
        if not self.running:
            from auction.tasks import start_auction
            start_auction.apply_async(args=[self.id, ], eta=self.start_time)


class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
