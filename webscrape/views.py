from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view

from .utils import clean_body_content, extract_body_content, parse_with_huggingface, scrape_website, split_dom_content
# from API.tasks import scrape_and_store
from .models import ScrapingTask, ScrapedData
from .serializers import ScrapingTaskSerializer, ScrapedDataSerializer

class ScrapingTaskViewSet(viewsets.ModelViewSet):
    """
    API for managing scraping tasks.
    """
    queryset = ScrapingTask.objects.all()
    serializer_class = ScrapingTaskSerializer

    @action(detail=False, methods=["GET"])
    def active_tasks(self, request):
        """List only active scraping tasks."""
        tasks = self.get_queryset().filter(active=True)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Create a new scraping task and schedule periodic execution."""
        task = serializer.save()
        # scrape_and_store.delay(task.id)  # Start scraping immediately

    @action(detail=True, methods=["POST"])
    def trigger_scrape(self, request, pk=None):
        """Manually trigger a scrape for a specific task."""
        task = self.get_object()
        scrape_and_store.delay(task.id)
        return Response({"message": f"Scraping started for {task.url}"})

class ScrapedDataViewSet(viewsets.ModelViewSet):
    queryset = ScrapedData.objects.all()
    serializer_class = ScrapedDataSerializer

    def get_queryset(self):
        """Allow filtering by URL."""
        url = self.request.GET.get("url")
        if url:
            return ScrapedData.objects.filter(task__url=url).order_by("-scraped_at")
        return super().get_queryset()


@api_view(["POST"])
def quick_scrape(request):
    """Scrape a URL once and process AI response immediately."""
    url = request.data.get("url")
    user_prompt = request.data.get("prompt")

    if not url or not user_prompt:
        return Response({"error": "URL and prompt are required"}, status=400)

    try:
        # Step 1: Scrape Website
        html_content = scrape_website(url)

        # Step 2: Extract and Clean Body Content
        body_content = extract_body_content(html_content)
        cleaned_text = clean_body_content(body_content)

        # Step 3: Split Content (if needed)
        dom_chunks = split_dom_content(cleaned_text)

        # Step 4: Pass to AI Model
        ai_response = parse_with_huggingface(dom_chunks, user_prompt)

        return Response({"url": url, "ai_response": ai_response})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


