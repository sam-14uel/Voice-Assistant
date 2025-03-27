from django.db import models


class ScrapingTask(models.Model):
    url = models.URLField(unique=True)  # Website to scrape
    interval = models.IntegerField(help_text="Interval in minutes")  # Frequency of scraping
    active = models.BooleanField(default=True)  # Toggle scraping on/off
    last_scraped = models.DateTimeField(blank=True, null=True)  # Last time scraped
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - Every {self.interval} min"

class ScrapedData(models.Model):
    task = models.ForeignKey(ScrapingTask, on_delete=models.CASCADE, related_name="scraped_entries")
    html_content = models.TextField(blank=True, null=True)  # Store HTML (optional)
    extracted_text = models.TextField()  # Processed text content
    metadata = models.JSONField(default=dict, blank=True)  # Store additional data (e.g., title, images)
    scraped_at = models.DateTimeField(auto_now_add=True)  # Timestamp of scraping

    def __str__(self):
        return f"Data from {self.task.url} - {self.scraped_at}"
