from rest_framework import serializers
from django.utils import timezone
from .models import IntegrationAccount

class SchedulePostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    platform_id = serializers.CharField(max_length=128)
    scheduled_time = serializers.DateTimeField()

    def validate_scheduled_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future")
        return value

    def validate_platform_id(self, value):
        user = self.context['request'].user
        try:
            IntegrationAccount.objects.get(integration_account_id=value, user=user)
        except IntegrationAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid platform or platform does not belong to the user")
        return value