# models.py
from django.db import models
from django.contrib.auth.models import User
from djstripe.models import Subscription

class Plan(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)  # Dynamic price reference from Stripe
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

from django.db import models
from djstripe.models import Customer

class SubscriptionManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    plan = models.CharField(max_length=20, choices=[("free", "Free"), ("basic", "Basic"), ("standard", "Standard")], default="free")
    created_at = models.DateTimeField(auto_now_add=True)


class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals_sent")
    referee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals_received")
    code = models.ForeignKey(ReferralCode, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=[("basic", "Basic"), ("standard", "Standard")], null=True, blank=True)
    reward_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)