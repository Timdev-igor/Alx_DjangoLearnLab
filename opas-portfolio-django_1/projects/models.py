from django.db import models
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to="projects/")
    summary = models.CharField(max_length=300, help_text="Short blurb shown on the grid card")
    description = models.TextField(blank=True, help_text="Full write-up on the detail page")
    tech_stack = models.CharField(
        max_length=300, blank=True, help_text="Comma-separated, e.g. 'Django, DRF, Celery, Azure'"
    )
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False, help_text="Pin to the top of the grid")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "order", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.slug])

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]
