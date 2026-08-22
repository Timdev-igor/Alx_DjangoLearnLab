from django.conf import settings
from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = getattr(settings, "BLOG_PAGE_SIZE", 9)

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
