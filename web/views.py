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


import json
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required

from .llm import ask_llm_text
from .models import ChatLog


@staff_member_required
def chat_page(request: HttpRequest):
    """
    /chat/ : 테스트 UI 페이지

    ✅ staff_member_required 의미
    - 로그인 안 했으면: admin 로그인 페이지로 리다이렉트됨
    - 로그인 했어도 staff 아니면: 접근 불가
    """
    return render(request, "web/chat.html")


@require_POST
@csrf_protect
@staff_member_required
def chat_api(request: HttpRequest):
    # 1) JSON 바디 파싱
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    prompt = (body.get("prompt") or "").strip()

    # 2) 입력 검증
    if not prompt:
        return JsonResponse({"error": "prompt is required"}, status=400)
    if len(prompt) > 3000:
        return JsonResponse({"error": "prompt too long (max 3000 chars)"}, status=400)

    # 3) LLM 호출 (✅ 텍스트만 받음)
    try:
        answer, latency_ms = ask_llm_text(prompt, model="gpt-5-chat-latest")
    except BadRequestError as e:
        print("=== OpenAI BadRequestError ===")
        print("str(e):", str(e))
        print("repr(e):", repr(e))
        print("=== traceback ===")
        traceback.print_exc()
        return JsonResponse({"error": "OpenAI BadRequestError - check server logs"}, status=500)
    except Exception:
        print("=== Unexpected error ===")
        traceback.print_exc()
        return JsonResponse({"error": "LLM call failed - check server logs"}, status=500)

    # 4) DB 저장 (✅ response_text 필드에 answer 저장)
    ChatLog.objects.create(
        user=request.user,
        prompt=prompt,
        response_text=answer,
        model="gpt-5-chat-latest",
        latency_ms=latency_ms,
    )

    # 5) JSON 응답 (프론트는 res.json() 가능)
    return JsonResponse({"answer": answer, "latency_ms": latency_ms})