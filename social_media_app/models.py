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
    

class IntegrationAccount(models.Model):
    """
    Model to store access tokens for user accounts on different integration platforms.
    """
    platform = models.ForeignKey(IntegrationPlatform, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
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
    platforms = models.ManyToManyField(IntegrationAccount)  # Which platforms to post to
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
    platform_account = models.ForeignKey(IntegrationAccount, on_delete=models.CASCADE, related_name='scheduled_posts')
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


#============================================================================================
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    """Company/Brand information model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    description = models.TextField()
    mission_statement = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
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
    
    def __str__(self):
        return f"{self.company.name}'s Target Audience"

class SocialMediaProfile(models.Model):
    """Social media platform details"""
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('snapchat', 'Snapchat'),
        ('other', 'Other'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='social_profiles')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    profile_url = models.URLField()
    username = models.CharField(max_length=100)
    audience_size = models.PositiveIntegerField(default=0)
    posting_frequency = models.CharField(max_length=50, blank=True, null=True)
    platform_specific_guidelines = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['company', 'platform']
    
    def __str__(self):
        return f"{self.company.name} on {self.platform}"

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
    
    def __str__(self):
        return f"{self.name} - competitor of {self.company.name}"

class UniqueSellingProposition(models.Model):
    """Unique selling proposition"""
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='usp')
    main_usp = models.TextField(help_text="What makes your company/product unique?")
    differentiators = models.TextField(help_text="Key differentiators from competitors")
    value_proposition = models.TextField(help_text="Value you provide to customers")
    
    def __str__(self):
        return f"{self.company.name}'s USP"

class ContentAsset(models.Model):
    """Content assets for social media posts"""
    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('testimonial', 'Testimonial'),
        ('case_study', 'Case Study'),
        ('other', 'Other'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='content_assets')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='content_assets/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.company.name}"

class PostTemplate(models.Model):
    """Template for generated posts"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='post_templates')
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50)
    template_text = models.TextField()
    post_type = models.CharField(max_length=50)
    character_limit = models.PositiveIntegerField(default=0)
    image_specs = models.CharField(max_length=255, blank=True, null=True)
    hashtag_strategy = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"
#============================================================================================