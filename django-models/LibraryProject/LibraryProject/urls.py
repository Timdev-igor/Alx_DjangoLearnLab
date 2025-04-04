"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.shortcuts import redirect
from django.views.generic import TemplateView
from relationship_app.views import admin_view, librarian_view, member_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("relationship_app/", include("relationship_app.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", TemplateView.as_view(template_name="authentication/profile.html"), name="profile"), 
    path("admin_view/", admin_view, name="admin_view"),
    path("librarian_view/", librarian_view, name="librarian_view"),
    path("member_view/", member_view, name="member_view"),
]

