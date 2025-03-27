from django.db import models
from django.contrib.auth.models import User
import shortuuid
import uuid
import json
from django.utils import timezone
from ai_agent.models import Task

class SocialMedia(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    

class SocialMediaAccount(models.Model):
    platform = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class PostDraft(models.Model):
    """Model for content drafts waiting for approval"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    )
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_drafts')
    related_task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, related_name='post_drafts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    media_urls = models.JSONField(blank=True, null=True)  # List of media URLs to attach
    platforms = models.ManyToManyField(SocialMediaAccount)  # Which platforms to post to
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user_feedback = models.TextField(blank=True, null=True)  # User feedback for revisions
   
    def __str__(self):
        return f"{self.title} - {self.status}"

class ScheduledPost(models.Model):
    """Model for approved posts scheduled for publishing"""
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
   
    post_draft = models.ForeignKey(PostDraft, on_delete=models.CASCADE, related_name='scheduled_posts')
    platform_account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE, related_name='scheduled_posts')
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    published_at = models.DateTimeField(blank=True, null=True)
    post_id = models.CharField(max_length=100, blank=True, null=True)  # ID from the platform after posting
    engagement_metrics = models.JSONField(blank=True, null=True)  # Metrics after publishing
    error_message = models.TextField(blank=True, null=True)
   
    class Meta:
        ordering = ['scheduled_time']
       
    def __str__(self):
        return f"{self.post_draft.title} - {self.platform_account.platform.name} - {self.status}"