from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("", include("sveve.urls"))]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
