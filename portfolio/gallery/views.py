from django.conf import settings
from django.db.models import F
from django.views.generic import DetailView, ListView

from .models import Artwork


class GalleryListView(ListView):
    """
    Paginated, filterable masonry grid. Reads ?type=... and ?year=...
    from the querystring (set by the Type/Year filter links in the
    template) and filters the queryset server-side — no JS involved.
    """
    model = Artwork
    template_name = "gallery/list.html"
    context_object_name = "artworks"
    paginate_by = getattr(settings, "GALLERY_PAGE_SIZE", 12)

    def get_queryset(self):
        qs = Artwork.objects.all()
        selected_type = self.request.GET.get("type", "all")
        selected_year = self.request.GET.get("year", "all")

        if selected_type != "all":
            qs = qs.filter(category=selected_type)
        if selected_year != "all":
            qs = qs.filter(year=selected_year)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_type"] = self.request.GET.get("type", "all")
        context["selected_year"] = self.request.GET.get("year", "all")
        context["type_choices"] = Artwork.TYPE_CHOICES
        context["year_choices"] = (
            Artwork.objects.order_by("-year").values_list("year", flat=True).distinct()
        )
        return context


class ArtworkDetailView(DetailView):
    """
    Single art-view page. Increments the view counter atomically on every
    load using F() so two simultaneous visitors can't stomp on each other's
    increment (same race-condition-safe pattern used elsewhere in the
    ecommerce project's stock/checkout logic).
    """
    model = Artwork
    template_name = "gallery/detail.html"
    context_object_name = "artwork"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Artwork.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        obj.refresh_from_db(fields=["views"])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description_lines"] = [
            line for line in self.object.description.splitlines() if line.strip()
        ]
        return context
