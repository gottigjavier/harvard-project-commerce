from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Auction(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30, default='uncategorized')
    description = models.CharField(max_length=300)
    init_bid = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    is_open = models.BooleanField(default=True)
    delivered = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now)
    offerer = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    follower = models.ManyToManyField(User)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(default=datetime.now)
    who_bid = models.ForeignKey(User, on_delete=models.CASCADE)
    for_auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return self.for_auction.name

class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    who_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    for_auction = models.ForeignKey(Auction, on_delete=models.CASCADE)