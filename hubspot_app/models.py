from django.db import models
from django.contrib.auth.models import User

class HubSpotAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)

    def __str__(self):
        return self.account_name