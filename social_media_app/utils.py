import facebook
import tweepy
import requests


class SocialMediaClient:
    def post_on_facebook(self, access_token, message):
        url = f"https://graph.facebook.com/v12.0/me/feed"
        data = {"message": message, "access_token": access_token}
        response = requests.post(url, data=data)
        return response.json()


    def post_on_linkedin(self, access_token, message):
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


    def post_on_instagram(self, access_token, image_url, caption):
        url = f"https://graph.facebook.com/v12.0/me/media"
        data = {"image_url": image_url, "caption": caption, "access_token": access_token}
        media_response = requests.post(url, data=data).json()

        publish_url = f"https://graph.facebook.com/v12.0/me/media_publish"
        publish_data = {"creation_id": media_response["id"], "access_token": access_token}
        publish_response = requests.post(publish_url, data=publish_data)
        
        return publish_response.json()


    def post_on_twitter(self, access_token, message):
        url = "https://api.twitter.com/2/tweets"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"text": message}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    # comment replies
    def reply_comment_on_facebook(self):
        pass

    def reply_comment_on_linkedin(self):
        pass

    def reply_comment_on_instagram(self):
        pass

    def reply_comment_on_twitter(self, access_token, tweet_id, message):
        url = "https://api.twitter.com/2/tweets"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"text": message, "reply": {"in_reply_to_tweet_id": tweet_id}}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    # comment reactions
    def react_on_facebook_comment(self, access_token, comment_id):
        url = f"https://graph.facebook.com/v12.0/{comment_id}/reactions"
        data = {"type":"LIKE",  # Options: LIKE/LOVE/WOW etc.
                "access_token": access_token}
        
        response=requests.post(url,data)


    def react_on_linkedin_comment(self):
        pass

    def react_on_instagram_comment(self):
        pass

    def react_on_twitter_comment(self, access_token, tweet_id):
        url = f"https://api.twitter.com/2/users/me/likes"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {"tweet_id": tweet_id}
        response = requests.post(url, json=data, headers=headers)
        return response.json()
