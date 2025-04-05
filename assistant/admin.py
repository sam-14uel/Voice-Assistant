from django.contrib import admin
from ai_agent.models import Task, TaskWorkflow, Chat, ChatRoom
from social_media_app.models import (
    IntegrationPlatform, IntegrationAccount, Post, ScheduledPost,
    Company, BrandIdentity, TargetAudience, ContentStrategy

)

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_type', 'status', 'created_at', 'scheduled_for', 'executed_at')
    list_filter = ('status', 'created_at', 'task_type')
    search_fields = ('title', 'description', 'task_type')
    #ordering = ('-created_at')

class TaskWorkflowAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'status', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'status')
    #ordering = ('-created_at')

class ChatAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'created', 'chat_id')
    list_filter = ('created', 'media_is_img', 'media_is_aud', 'media_is_doc', 'media_is_vid')
    search_fields = ('sender', 'room', 'text')
    #ordering = ('-created')

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created', 'is_private')
    list_filter = ('created', 'is_private')
    search_fields = ('group_name', 'group_decription')
    #ordering = ('-created')

class IntegrationPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'last_updated')
    # search_fields = ('name')

class IntegrationAccountAdmin(admin.ModelAdmin):
    list_display = ('platform', 'user', 'created_at')
    list_filter = ('created_at', 'platform')
    search_fields = ('platform', 'user')
    #ordering = ('-created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content')
    #ordering = ('-created_at')

class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = ('post_draft', 'platform_account', 'scheduled_time', 'status', 'published_at')
    list_filter = ('status', 'scheduled_time', 'published_at')
    search_fields = ('post_draft', 'platform_account')
    #ordering = ('-scheduled_time')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'industry', 'founded_year')
    search_fields = ('name', 'industry')
    list_filter = ('industry', 'founded_year')

    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'description', 'mission_statement', 'industry', 'website', 'founded_year', 'company_size', 'logo')
        }),
    )

class BrandIdentityAdmin(admin.ModelAdmin):
    list_display = ('company', 'brand_voice', 'color_palette')
    search_fields = ('company__name', 'brand_voice')
    list_filter = ('brand_voice',)

    ordering = ('company',)
    fieldsets = (
        (None, {
            'fields': ('company', 'brand_voice', 'brand_voice_details', 'brand_values', 'color_palette', 'typography', 'visual_style')
        }),
    )


admin.site.register(IntegrationPlatform, IntegrationPlatformAdmin)
admin.site.register(IntegrationAccount, IntegrationAccountAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ScheduledPost, ScheduledPostAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskWorkflow, TaskWorkflowAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Company)
admin.site.register(BrandIdentity)
admin.site.register(TargetAudience)
admin.site.register(ContentStrategy)