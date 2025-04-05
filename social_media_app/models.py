from django.db import models
from django.contrib.auth.models import User
import shortuuid
import uuid
import json
from django.utils import timezone
from ai_agent.models import Task

class IntegrationPlatform(models.Model):
    """
    Model to represent different integration platforms, including CRM and social media.
    """
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    api_endpoint = models.URLField(null=True, blank=True)  # e.g., "https://api.twitter.com/2/tweets"
    max_length = models.IntegerField(default=280)  # e.g., Twitter: 280, Instagram: 2200
    platform_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    

class IntegrationAccount(models.Model):
    """
    Model to store access tokens for user accounts on different integration platforms.
    """
    platform = models.ForeignKey(IntegrationPlatform, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)  # For OAuth refresh
    expires_at = models.DateTimeField(null=True, blank=True)  # Token expiration
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    integration_account_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)

class Post(models.Model):
    """"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_drafts')
    content = models.TextField()
    media_urls = models.JSONField(blank=True, null=True)  # List of media URLs to attach
    platforms = models.ForeignKey(IntegrationAccount, on_delete=models.CASCADE)  # Which platforms to post to
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    post_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
   
    def __str__(self):
        return f"Post {self.post_id} by {self.user.username} post on {self.platforms.platform.name}"


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="media/%Y/%m/%d/")
    media_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for Post {self.post.post_id}"

class ScheduledPost(models.Model):
    """Model for approved posts scheduled for publishing"""
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='scheduled_posts')
    platform_account = models.ForeignKey(IntegrationAccount, on_delete=models.CASCADE, related_name='scheduled_posts')
    scheduled_time = models.DateTimeField() # When the post should go live
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)  # Actual publish time
    platform_post_id = models.CharField(max_length=100, blank=True, null=True)  # ID from the platform after posting
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    schedule_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
   
    class Meta:
        ordering = ['scheduled_time']
       
    def __str__(self):
        return f"Scheduled {self.post.post_id} at {self.scheduled_time}"


class PostAnalytics(models.Model):
    scheduled_post = models.ForeignKey(ScheduledPost, on_delete=models.CASCADE)
    integration_account = models.ForeignKey(IntegrationAccount, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    last_fetched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.scheduled_post.post.post_id} on {self.integration_account.platform.name}"


#============================================================================================
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    """Company/Brand information model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    description = models.TextField()
    mission_statement = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return self.name

class BrandIdentity(models.Model):
    """Brand voice, values, and visual identity"""
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('friendly', 'Friendly'),
        ('humorous', 'Humorous'),
        ('inspirational', 'Inspirational'),
        ('authoritative', 'Authoritative'),
        ('innovative', 'Innovative'),
        ('formal', 'Formal'),
    ]
    brand_identity_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='brand_identity')
    brand_voice = models.CharField(max_length=50, choices=TONE_CHOICES)
    brand_voice_details = models.TextField(help_text="Additional details about your brand voice")
    brand_values = models.TextField(help_text="List your core brand values, separated by commas")
    color_palette = models.CharField(max_length=255, blank=True, null=True, help_text="Brand colors (hex codes preferred)")
    typography = models.CharField(max_length=255, blank=True, null=True, help_text="Brand fonts")
    visual_style = models.TextField(help_text="Describe your preferred visual aesthetic")
    
    def __str__(self):
        return f"{self.company.name}'s Brand Identity"

class TargetAudience(models.Model):
    """Target audience demographics and psychographics"""
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='target_audience')
    age_range = models.CharField(max_length=50, blank=True, null=True)
    gender_demographics = models.CharField(max_length=100, blank=True, null=True)
    geographic_locations = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    pain_points = models.TextField(blank=True, null=True)
    behavior_patterns = models.TextField(blank=True, null=True)
    target_audience_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return f"{self.company.name}'s Target Audience"


class ContentStrategy(models.Model):
    """Content strategy and goals"""
    GOAL_CHOICES = [
        ('awareness', 'Brand Awareness'),
        ('engagement', 'Engagement'),
        ('traffic', 'Website Traffic'),
        ('leads', 'Lead Generation'),
        ('sales', 'Sales/Conversions'),
        ('loyalty', 'Customer Loyalty'),
        ('community', 'Community Building'),
        ('other', 'Other'),
    ]
    
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='content_strategy')
    primary_goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    secondary_goals = models.CharField(max_length=100, blank=True, null=True)
    content_pillars = models.TextField(help_text="Main themes/topics for your content")
    key_messages = models.TextField(help_text="Core messages to communicate")
    preferred_post_types = models.TextField(help_text="e.g., Educational, Promotional, UGC, etc.")
    content_to_avoid = models.TextField(blank=True, null=True)
    campaign_info = models.TextField(blank=True, null=True, help_text="Current or upcoming campaigns")
    content_strategy_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return f"{self.company.name}'s Content Strategy"

class Product(models.Model):
    """Products or services to highlight"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    key_features = models.TextField()
    target_audience = models.TextField(blank=True, null=True)
    price_info = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Competitor(models.Model):
    """Information about competitors"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='competitors')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    strengths = models.TextField(blank=True, null=True)
    weaknesses = models.TextField(blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)
    competitor_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return f"{self.name} - competitor of {self.company.name}"

class UniqueSellingProposition(models.Model):
    """Unique selling proposition"""
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='usp')
    main_usp = models.TextField(help_text="What makes your company/product unique?")
    differentiators = models.TextField(help_text="Key differentiators from competitors")
    value_proposition = models.TextField(help_text="Value you provide to customers")
    unique_selling_proposition_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    
    def __str__(self):
        return f"{self.company.name}'s USP"

#============================================================================================

