from django.contrib import admin
from django.urls import path, include
from web.views import home, health_db

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/db/", health_db, name="health_db"),
    path("", include("web.urls")),   
]