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
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Bids(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
