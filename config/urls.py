from django.contrib import admin
from django.urls import path
from web.views import home

# 어드민 외 기본 경로 추가
urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="", view=home, name="home"),
]
