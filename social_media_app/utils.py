import facebook
import tweepy
import requests
import json

class SocialMediaClient:
    def post_on_facebook(self, access_token, message):
        try:
            url = f"https://graph.facebook.com/v12.0/me/feed"
            data = {"message": message, "access_token": access_token}
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            return f"Error posting on Facebook: {str(e)}"


    def post_on_linkedin(self, access_token, message):
        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            data = {
                "author": "urn:li:person:<your-person-id>",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": message},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }
            response = requests.post(url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error posting on LinkedIn: {str(e)}"


    def post_on_instagram(self, access_token, image_url, caption):
        try:
            url = f"https://graph.facebook.com/v12.0/me/media"
            data = {"image_url": image_url, "caption": caption, "access_token": access_token}
            media_response = requests.post(url, data=data).json()

            publish_url = f"https://graph.facebook.com/v12.0/me/media_publish"
            publish_data = {"creation_id": media_response["id"], "access_token": access_token}
            publish_response = requests.post(publish_url, data=publish_data)
            
            return publish_response.json()
        except Exception as e:
            return f"Error posting on Instagram: {str(e)}"


    def post_on_twitter(self, access_token, message):
        try:
            url = "https://api.twitter.com/2/tweets"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {"text": message}
            response = requests.post(url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error posting on Twitter-X: {str(e)}"

    # comment replies
    def reply_comment_on_facebook(self, access_token, page_id, comment_id, message):
        try:
            url = f"https://graph.facebook.com/v20.0/{page_id}/messages"
            params = {
                "recipient": {"comment_id": comment_id},
                "message": {"text": message},
                "access_token": access_token
            }
            response = requests.post(url, json=params)
            return response.json()
        except Exception as e:
            return f"Error replying to comment '{comment_id}' on Facebook: {str(e)}"

    def reply_comment_on_linkedin(self, access_token, parent_id, message, actor_id):
        try:
            url = f"https://api.linkedin.com/v2/socialActions/{parent_id}/comments"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "message": {"text": message},
                "parentComment": parent_id,
                "actor": actor_id
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            return response.json()
        except Exception as e:
            return f"Error replying to comment on LinkedIn: {str(e)}"

    def reply_comment_on_instagram(self, access_token, media_id, message):
        try:
            url = f"https://graph.facebook.com/v20.0/{media_id}/comments"
            params = {
                "message": message,
                "access_token": access_token
            }
            response = requests.post(url, params=params)
            return response.json()
        except Exception as e:
            return f"Error replying to comment on Instagram: {str(e)}"

    def reply_comment_on_twitter(self, access_token, tweet_id, message):
        try:
            url = "https://api.twitter.com/2/tweets"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {"text": message, "reply": {"in_reply_to_tweet_id": tweet_id}}
            response = requests.post(url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error replying to tweet '{tweet_id}' on Twitter-X: {str(e)}"

    # comment reactions
    def react_on_facebook_comment(self, access_token, comment_id):
        try:
            url = f"https://graph.facebook.com/v12.0/{comment_id}/reactions"
            data = {"type":"LIKE",  # Options: LIKE/LOVE/WOW etc.
                    "access_token": access_token}
            
            response=requests.post(url,data)
        except Exception as e:
            return f"Error reacting to comment '{comment_id}' on Facebook: {str(e)}"


    def react_on_linkedin_comment(self, access_token, comment_id):
        try:
            url = f"https://api.linkedin.com/v2/socialActions/{comment_id}/likes"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error reacting to comment '{comment_id}' on LinkedIn: {str(e)}"

    def react_on_instagram_comment(self, access_token, comment_id):
        try:
            url = f"https://graph.facebook.com/v20.0/{comment_id}/likes"
            params = {"access_token": access_token}
            response = requests.post(url, params=params)
            return response.json()
        except Exception as e:
            return f"Error reacting to comment '{comment_id}' on Instagram: {str(e)}"

    def react_on_twitter_comment(self, access_token, tweet_id):
        try:
            url = f"https://api.twitter.com/2/users/me/likes"
            headers = {"Authorization": f"Bearer {access_token}"}
            data = {"tweet_id": tweet_id}
            response = requests.post(url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            return f"Error reacting to tweet '{tweet_id}' on Twitter-X: {str(e)}"
