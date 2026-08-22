from django.views.generic import ListView

from .models import Certificate


class CertificateListView(ListView):
    model = Certificate
    template_name = "certificates/list.html"
    context_object_name = "certificates"
