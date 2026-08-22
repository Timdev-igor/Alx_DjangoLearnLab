from django.db import models


class ResumeEntry(models.Model):
    SECTION_CHOICES = [
        ("experience", "Experience"),
        ("education", "Education"),
    ]

    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    date_range = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["section", "order"]
        verbose_name_plural = "Resume entries"

    def __str__(self):
        return f"{self.get_section_display()} — {self.title}"
