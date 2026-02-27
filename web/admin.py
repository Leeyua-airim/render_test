from django.contrib import admin
from .models import Note, ChatLog

admin.site.register(Note)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    """
    admin에서 로그를 보기 쉽게 설정.
    """
    list_display = ("id", "created_at", "user", "model", "latency_ms")
    list_filter = ("model", "created_at")
    search_fields = ("prompt", "response_json")
    ordering = ("-created_at",)