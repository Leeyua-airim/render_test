from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
import time

# 호출에 따른 응답 테스트
def home(request):
    return HttpResponse("Hello from Render")

def health_db(request):
    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        cursor.fetchone()
    ms = int((time.time() - start) * 1000)
    return JsonResponse({"status": "ok", "db": "ok", "latency_ms": ms})