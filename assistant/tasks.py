from celery import shared_task
import logging
logger = logging.getLogger(__name__)
from django.utils import timezone
from social_media_app.utils import SocialMediaClient

social_media_management_tool = SocialMediaClient()
client = social_media_management_tool

@shared_task
def check_due_facebook_post():
    now = timezone.now()
    client.post_on_facebook("access_token", "message")
    pass

@shared_task
def check_due_twitter_post():
    now = timezone.now()
    client.post_on_twitter("access_token", "message")
    pass

@shared_task
def check_due_linkedin_post():
    now = timezone.now()
    client.post_on_linkedin("access_token", "message")
    pass

@shared_task
def check_due_instagram_post():
    now = timezone.now()
    client.post_on_instagram("access_token", "image_url", "caption")
    pass


from celery import shared_task
from webscrape.models import ScrapingTask, ScrapedData
from webscrape.utils import scrape_website, extract_body_content, clean_body_content, split_dom_content
from django.utils.timezone import now

@shared_task
def scrape_and_store(task_id):
    """Scrape a website and store the extracted data without AI processing."""
    try:
        task = ScrapingTask.objects.get(id=task_id)
        if not task.active:
            return "Task is inactive."

        html = scrape_website(task.url)
        body_content = extract_body_content(html)
        cleaned_text = clean_body_content(body_content)
        dom_chunks = split_dom_content(cleaned_text)

        # Save raw scraped data
        ScrapedData.objects.create(task=task, extracted_text="\n".join(dom_chunks), scraped_at=now())

        # Update last scraped time
        task.last_scraped = now()
        task.save()

        return f"Scraping completed for {task.url}"

    except ScrapingTask.DoesNotExist:
        return "Scraping task not found."
