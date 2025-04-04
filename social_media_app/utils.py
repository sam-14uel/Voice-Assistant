# import facebook
# import tweepy
# from tweepy import Client
# from facebook import GraphAPI
# import requests
# import json

# class FacebookTools:
#     client = GraphAPI()

#     def get_profile(self):
#         try:
#             user = self.client.get_object("me")
#             response = user
#             return response
#         except Exception as e:
#             return f"Error getting profile info on Facebook: {str(e)}"

#     def get_profile_friends(self):
#         try:
#             user = self.client.get_object("me")
#             friends = self.client.get_connections(user["id"], "friends")
#             response = friends
#             return response
#         except Exception as e:
#             return f"Error getting profile friends on Facebook: {str(e)}"

#     def create_post(self, text):
#         try:
#             response = self.client.put_object(
#                 parent_object='me',
#                 connection_name='feed',
#                 message=text
#             )
#             return response
#         except Exception as e:
#             return f"Error creating post on Facebook: {str(e)}"

#     def reply_comment(self, text):
#         try:
#             response = self.client.put_object(
#                 parent_object='COMMENT_ID',
#                 connection_name='comments',
#                 message=text
#             )
#             return response
#         except Exception as e:
#             return f"Error replying comment on Facebook: {str(e)}"


# class TwitterTools:
#     client =  Client()
#     def create_tweet(self, text):
#         try:
#             response = self.client.create_tweet(text=text)
#             return response
#         except Exception as e:
#             return f"Error posting on Twitter-X: {str(e)}"
        
#     def delete_tweet(self, tweet_id):
#         try:
#             response = self.client.delete_tweet(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error deleting post on Twitter-X: {str(e)}"
        
#     def like_tweet(self, tweet_id):
#         try:
            
#             response = self.client.like(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error reacting to post '{tweet_id}' on Twitter-X: {str(e)}"
        
#     def unlike_tweet(self, tweet_id):
#         try:
#             response = self.client.unlike(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error unliking post '{tweet_id}' on Twitter-X: {str(e)}"
        

#     def follow(self, user_id):
#         try:
#             response = self.client.follow_user(user_id)
#             return response
#         except Exception as e:
#             return f"Error following '{user_id}' on Twitter-X: {str(e)}"

    
#     def unfollow(self, user_id):
#         try:
#             response = self.client.unfollow_user(user_id)
#             return response
#         except Exception as e:
#             return f"Error unfollowing '{user_id}' on Twitter-X: {str(e)}"
        

#     def retweet_tweet(self, tweet_id):
#         try:
#             response = self.client.retweet(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error reposting post '{tweet_id}' on Twitter-X: {str(e)}"
        

#     def unretweet_tweet(self, tweet_id):
#         try:
#             response = self.client.unretweet(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error unreposting post '{tweet_id}' on Twitter-X: {str(e)}"
        
#     def follow_list(self, list_id):
#         try:
#             response = self.client.follow_list(list_id)
#             return response
#         except Exception as e:
#             return f"Error following list '{list_id}' on Twitter-X: {str(e)}"
        
#     def unfollow_list(self, list_id):
#         try:
#             response = self.client.unfollow_list(list_id)
#             return response
#         except Exception as e:
#             return f"Error unfollowing list '{list_id}' on Twitter-X: {str(e)}"
        
#     def get_retweeters(self, tweet_id):
#         try:
#             response = self.client.get_retweeters(tweet_id)
#             return response
#         except Exception as e:
#             return f"Error getting reposters for '{tweet_id}' on Twitter-X: {str(e)}"
        
#     def search_users_by_username(self, username):
#         try:
#             response = self.client.get_users(usernames=username)
#             return response
#         except Exception as e:
#             return f"Error searching results for @'{username}' on Twitter-X: {str(e)}"
        
#     def get_user_by_username(self, username):
#         try:
#             response = self.client.get_user(username=username)
#             return response
#         except Exception as e:
#             return f"Error viewing @'{username}' on Twitter-X: {str(e)}"
        


# class LinkedInTools:
#     pass
        

# class InstagramTools:
#     pass


# class SocialMediaClient:
#     twitter_x_tools = TwitterTools()
#     linkedin_tools = LinkedInTools()
#     instagram_tools =  InstagramTools()
#     facebook_tools = FacebookTools()

#     def post_on_facebook(self, access_token, message):
#         try:
#             url = f"https://graph.facebook.com/v12.0/me/feed"
#             data = {"message": message, "access_token": access_token}
#             response = requests.post(url, data=data)
#             return response.json()
#         except Exception as e:
#             return f"Error posting on Facebook: {str(e)}"


#     def post_on_linkedin(self, access_token, message):
#         try:
#             url = "https://api.linkedin.com/v2/ugcPosts"
#             headers = {
#                 "Authorization": f"Bearer {access_token}",
#                 "Content-Type": "application/json",
#                 "X-Restli-Protocol-Version": "2.0.0",
#             }
#             data = {
#                 "author": "urn:li:person:<your-person-id>",
#                 "lifecycleState": "PUBLISHED",
#                 "specificContent": {
#                     "com.linkedin.ugc.ShareContent": {
#                         "shareCommentary": {"text": message},
#                         "shareMediaCategory": "NONE",
#                     }
#                 },
#                 "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
#             }
#             response = requests.post(url, json=data, headers=headers)
#             return response.json()
#         except Exception as e:
#             return f"Error posting on LinkedIn: {str(e)}"


#     def post_on_instagram(self, access_token, image_url, caption):
#         try:
#             url = f"https://graph.facebook.com/v12.0/me/media"
#             data = {"image_url": image_url, "caption": caption, "access_token": access_token}
#             media_response = requests.post(url, data=data).json()

#             publish_url = f"https://graph.facebook.com/v12.0/me/media_publish"
#             publish_data = {"creation_id": media_response["id"], "access_token": access_token}
#             publish_response = requests.post(publish_url, data=publish_data)
            
#             return publish_response.json()
#         except Exception as e:
#             return f"Error posting on Instagram: {str(e)}"


#     def post_on_twitter(self, access_token, message):
#         try:
#             url = "https://api.twitter.com/2/tweets"
#             headers = {"Authorization": f"Bearer {access_token}"}
#             data = {"text": message}
#             response = requests.post(url, json=data, headers=headers)
#             return response.json()
#         except Exception as e:
#             return f"Error posting on Twitter-X: {str(e)}"

#     # comment replies
#     def reply_comment_on_facebook(self, access_token, page_id, comment_id, message):
#         try:
#             url = f"https://graph.facebook.com/v20.0/{page_id}/messages"
#             params = {
#                 "recipient": {"comment_id": comment_id},
#                 "message": {"text": message},
#                 "access_token": access_token
#             }
#             response = requests.post(url, json=params)
#             return response.json()
#         except Exception as e:
#             return f"Error replying to comment '{comment_id}' on Facebook: {str(e)}"

#     def reply_comment_on_linkedin(self, access_token, parent_id, message, actor_id):
#         try:
#             url = f"https://api.linkedin.com/v2/socialActions/{parent_id}/comments"
#             headers = {
#                 "Authorization": f"Bearer {access_token}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "message": {"text": message},
#                 "parentComment": parent_id,
#                 "actor": actor_id
#             }
#             response = requests.post(url, headers=headers, data=json.dumps(payload))
#             return response.json()
#         except Exception as e:
#             return f"Error replying to comment on LinkedIn: {str(e)}"

#     def reply_comment_on_instagram(self, access_token, media_id, message):
#         try:
#             url = f"https://graph.facebook.com/v20.0/{media_id}/comments"
#             params = {
#                 "message": message,
#                 "access_token": access_token
#             }
#             response = requests.post(url, params=params)
#             return response.json()
#         except Exception as e:
#             return f"Error replying to comment on Instagram: {str(e)}"

#     def reply_comment_on_twitter(self, access_token, tweet_id, message):
#         try:
#             url = "https://api.twitter.com/2/tweets"
#             headers = {"Authorization": f"Bearer {access_token}"}
#             data = {"text": message, "reply": {"in_reply_to_tweet_id": tweet_id}}
#             response = requests.post(url, json=data, headers=headers)
#             return response.json()
#         except Exception as e:
#             return f"Error replying to tweet '{tweet_id}' on Twitter-X: {str(e)}"

#     # comment reactions
#     def react_on_facebook_comment(self, access_token, comment_id):
#         try:
#             url = f"https://graph.facebook.com/v12.0/{comment_id}/reactions"
#             data = {"type":"LIKE",  # Options: LIKE/LOVE/WOW etc.
#                     "access_token": access_token}
            
#             response=requests.post(url,data)
#         except Exception as e:
#             return f"Error reacting to comment '{comment_id}' on Facebook: {str(e)}"


#     def react_on_linkedin_comment(self, access_token, comment_id):
#         try:
#             url = f"https://api.linkedin.com/v2/socialActions/{comment_id}/likes"
#             headers = {"Authorization": f"Bearer {access_token}"}
#             response = requests.post(url, headers=headers)
#             return response.json()
#         except Exception as e:
#             return f"Error reacting to comment '{comment_id}' on LinkedIn: {str(e)}"

#     def react_on_instagram_comment(self, access_token, comment_id):
#         try:
#             url = f"https://graph.facebook.com/v20.0/{comment_id}/likes"
#             params = {"access_token": access_token}
#             response = requests.post(url, params=params)
#             return response.json()
#         except Exception as e:
#             return f"Error reacting to comment '{comment_id}' on Instagram: {str(e)}"

#     def react_on_twitter_comment(self, access_token, tweet_id):
#         try:
#             url = f"https://api.twitter.com/2/users/me/likes"
#             headers = {"Authorization": f"Bearer {access_token}"}
#             data = {"tweet_id": tweet_id}
#             response = requests.post(url, json=data, headers=headers)
#             return response.json()
#         except Exception as e:
#             return f"Error reacting to tweet '{tweet_id}' on Twitter-X: {str(e)}"



# myapp/utils/social_media_utils.py
import requests
from django.conf import settings
from .models import PostAnalytics

# Base API endpoints (could also be stored in IntegrationPlatform model)
TWITTER_API_URL = "https://api.twitter.com/2/tweets"
FACEBOOK_API_URL = "https://graph.facebook.com/v20.0/me/feed"
INSTAGRAM_API_URL = "https://graph.instagram.com/v20.0/me/media"
LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"

# Utility functions for posting
def post_on_twitter(access_token, content, max_length, media=None):
    """
    Post content to Twitter/X.
    Returns: Response data or raises an exception on failure.
    """
    url = TWITTER_API_URL
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"text": content[:max_length]}
    
    if media:
        # Twitter media upload requires a separate API call first
        # Placeholder for media upload logic
        pass
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def post_on_facebook(access_token, content, max_length, media=None):
    """
    Post content to Facebook.
    """
    url = FACEBOOK_API_URL
    payload = {
        "message": content[:max_length],
        "access_token": access_token
    }
    if media:
        payload["url"] = media.file.url  # Assuming media.file.url gives the file path
    
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def post_on_instagram(access_token, content, max_length, media=None):
    """
    Post content to Instagram.
    Note: Instagram requires media upload first for images/videos.
    """
    url = INSTAGRAM_API_URL
    payload = {"caption": content[:max_length], "access_token": access_token}
    
    if media:
        payload["image_url"] = media.file.url  # Simplified; real flow needs media creation first
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def post_on_linkedin(access_token, content, max_length, media=None):
    """
    Post content to LinkedIn.
    """
    url = LINKEDIN_API_URL
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "author": "urn:li:person:{user_id}",  # Replace with actual user ID logic
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content[:max_length]},
                "shareMediaCategory": "NONE" if not media else "ARTICLE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    
    if media:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {"status": "READY", "media": media.file.url}
        ]
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Utility functions for fetching analytics
def fetch_twitter_analytics(access_token, post_id, scheduled_post, integration_account):
    """
    Fetch analytics for a Twitter post.
    """
    url = f"{TWITTER_API_URL}/{post_id}"  # Use actual tweet ID from post response
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params={"tweet.fields": "public_metrics"})
    response.raise_for_status()
    data = response.json()["data"]["public_metrics"]
    
    PostAnalytics.objects.update_or_create(
        scheduled_post=scheduled_post,
        integration_account=integration_account,
        defaults={
            "likes": data.get("like_count", 0),
            "shares": data.get("retweet_count", 0),
            "comments": data.get("reply_count", 0),
        }
    )

def fetch_facebook_analytics(access_token, post_id, scheduled_post, integration_account):
    """
    Fetch analytics for a Facebook post.
    """
    url = f"https://graph.facebook.com/v20.0/{post_id}/insights"
    params = {
        "metric": "post_reactions_by_type_total,post_impressions,post_comments",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()["data"]
    
    likes = data[0]["values"][0]["value"].get("like", 0) if data else 0
    shares = data[1]["values"][0]["value"] if len(data) > 1 else 0
    comments = data[2]["values"][0]["value"] if len(data) > 2 else 0
    
    PostAnalytics.objects.update_or_create(
        scheduled_post=scheduled_post,
        integration_account=integration_account,
        defaults={"likes": likes, "shares": shares, "comments": comments}
    )

def fetch_instagram_analytics(access_token, post_id, scheduled_post, integration_account):
    """
    Fetch analytics for an Instagram post.
    """
    url = f"https://graph.instagram.com/{post_id}/insights"
    params = {
        "metric": "likes,shares,comments",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()["data"]
    
    likes = data[0]["values"][0]["value"] if data else 0
    shares = data[1]["values"][0]["value"] if len(data) > 1 else 0
    comments = data[2]["values"][0]["value"] if len(data) > 2 else 0
    
    PostAnalytics.objects.update_or_create(
        scheduled_post=scheduled_post,
        integration_account=integration_account,
        defaults={"likes": likes, "shares": shares, "comments": comments}
    )

def fetch_linkedin_analytics(access_token, post_id, scheduled_post, integration_account):
    """
    Fetch analytics for a LinkedIn post.
    """
    url = f"https://api.linkedin.com/v2/shares/{post_id}/activity"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()  # Adjust based on LinkedIn API response
    
    PostAnalytics.objects.update_or_create(
        scheduled_post=scheduled_post,
        integration_account=integration_account,
        defaults={
            "likes": data.get("likes", 0),  # Placeholder fields
            "shares": data.get("shares", 0),
            "comments": data.get("comments", 0),
        }
    )