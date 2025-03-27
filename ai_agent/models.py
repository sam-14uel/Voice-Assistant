from django.db import models
from django.contrib.auth.models import User
import shortuuid
import uuid
import json
from django.utils import timezone

# Create your models here.


class ChatRoom(models.Model):
    room_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='chat_groups')

    group_name = models.CharField(max_length=128, blank=True, null=True)
    group_description = models.TextField(blank=True)
    group_picture = models.ImageField(default='media/default_group_pic.png', null=True, blank=True)
    is_private = models.BooleanField(default=False)
    private_group = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_private:
            members = self.members.exclude(username = self.admin.username)
            for member in members:
                return f"{self.admin.username} started a private conversation with {member.username}"
        elif self.is_private == False:
            return f"{self.group_name} Group was created by {self.admin.username}"
        else:
            return f"private group = {self.is_private}  with id = {self.room_id} created by {self.admin.username}"
        return f"private group = {self.is_private}  with id = {self.room_id} created by {self.admin.username}"

class Chat(models.Model):
    chat_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField(null=True)
    media = models.ManyToManyField('ChatMedia', blank=True)

    media_is_img = models.BooleanField(default=False)
    media_is_vid = models.BooleanField(default=False)
    media_is_aud = models.BooleanField(default=False)
    media_is_doc = models.BooleanField(default=False)

    task_workflow = models.ForeignKey(
        'TaskWorkflow',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_messages'
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.room.is_private:
            receivers = self.room.members.exclude(username = self.sender.username)
            for receiver in receivers:
                return f"from {self.sender.username} to {receiver.username}"
        elif self.room.is_private == False:
            return f"from {self.sender.username} to {self.room.group_name} Group created by {self.room.admin.username}"
        else:
            return f"from {self.sender.username} to {self.room.room_id}"
        return f"from {self.sender.username} to {self.room.room_id}"
    

class ChatMedia(models.Model):
    media = models.FileField(upload_to='media/chatroom_msg_media', null=True) 

    media_is_img = models.BooleanField(default=False)
    media_is_vid = models.BooleanField(default=False)
    media_is_aud = models.BooleanField(default=False)
    media_is_doc = models.BooleanField(default=False)

    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_media')

    media_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class TaskWorkflow(models.Model):
    """Model to store a sequence of tasks extracted from user prompts"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_workflows')
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='task_workflows')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    workflow_sequence = models.JSONField(default=dict)
    task_work_flow_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
   
    def __str__(self):
        return f"{self.title} - {self.status}"

class Task(models.Model):
    """Model to store individual tasks within a workflow"""
    TASK_TYPE_CHOICES = (
        ('hubspot_contact', 'Create Hubspot Contact'),
        ('post_content', 'Generate Post Content'),
        ('schedule_post', 'Schedule Post'),
        ('immediate_post', 'Post Immediately'),
        ('audience_analysis', 'Audience Analysis'),
        ('other', 'Other'),
    )
   
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workflow = models.ForeignKey(TaskWorkflow, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    sequence_number = models.PositiveIntegerField()  # Order in workflow
    description = models.TextField()
    function_name = models.CharField(max_length=100)  # Name of function to execute
    parameters = models.JSONField()  # Parameters for the function
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)  # When to execute
    executed_at = models.DateTimeField(blank=True, null=True)  # When executed
    result = models.JSONField(blank=True, null=True)  # Result of the task
    error_message = models.TextField(blank=True, null=True)  # If task failed
    task_id = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
   
    class Meta:
        ordering = ['workflow', 'sequence_number']
       
    def __str__(self):
        return f"{self.task_type} - {self.status}"