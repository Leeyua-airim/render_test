from django.http import HttpResponse

# 호출에 따른 응답 테스트
def home(request):
    return HttpResponse("Hello from Render")