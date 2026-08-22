from django.conf import settings
from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = getattr(settings, "PROJECTS_PAGE_SIZE", 9)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"
