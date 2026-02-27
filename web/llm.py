import os
import time
from typing import Literal, List

from pydantic import BaseModel, Field
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# print(client, "OpenAI client initialized")

def ask_llm_text(prompt: str, model: str = "gpt-5-chat-latest") -> tuple[str, int]:
    """
    LLM에 prompt를 보내고, '그냥 텍스트 답변'만 받는다.
    반환: (answer_text, latency_ms)

    ✅ JSON/스키마/파싱이 없어서 가장 안정적으로 동작함.
    """

    t0 = time.time()

    instructions = (
        "너는 보이스피싱/사기 예방을 돕는 상담 도우미다. "
        "항상 한국어로 답한다. "
        "위험하면 즉시 중단/차단/신고 등 안전 행동을 우선 안내한다."
    )

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=prompt,
        # ✅ text.format 지정 안 함 = 일반 텍스트 출력
    )

    latency_ms = int((time.time() - t0) * 1000)

    # ✅ output_text는 최종 텍스트만 편하게 꺼내주는 헬퍼
    return resp.output_text, latency_ms