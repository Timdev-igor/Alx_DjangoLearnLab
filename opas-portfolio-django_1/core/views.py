from django.views.generic import TemplateView

from blog.models import Post
from gallery.models import Artwork
from projects.models import Project

from .models import ResumeEntry


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.filter(featured=True)[:4]
        context["latest_posts"] = Post.objects.filter(is_published=True)[:3]
        context["latest_artworks"] = Artwork.objects.all()[:8]
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experience"] = ResumeEntry.objects.filter(section="experience")
        context["education"] = ResumeEntry.objects.filter(section="education")
        return context
