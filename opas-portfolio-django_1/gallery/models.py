from django.db import models
from django.urls import reverse


class Artwork(models.Model):
    TYPE_CHOICES = [
        ("illustration", "Illustration"),
        ("character", "Character"),
        ("concept", "Concept Art"),
        ("poster", "Poster"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Used in the URL, e.g. year-one")
    image = models.ImageField(upload_to="gallery/")

    code_name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Shown under the tile in the gallery grid, e.g. Andrevisuals#001A",
    )
    category = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="illustration",
        help_text="Powers the Type filter, and 'Filed under <category>' on the detail page.",
    )
    year = models.PositiveIntegerField(help_text="Powers the Year filter")

    # Powers the meta block on the detail page:
    # "Produced for... / Curated by... / dates / venue"
    description = models.TextField(
        blank=True,
        help_text="One line per paragraph, e.g. 'Produced for the Life in 2050 exhibition.'",
    )

    views = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallery:detail", args=[self.slug])
