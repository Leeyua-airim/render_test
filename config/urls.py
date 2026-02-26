from django.contrib import admin
from django.urls import path
from web.views import home, health_db

# 어드민 외 기본 경로 추가
urlpatterns = [
    
    path(route="", view=home, name="home"),
    path(route="admin/", view=admin.site.urls),
    path("health/db/", health_db, name="health_db"),

]
