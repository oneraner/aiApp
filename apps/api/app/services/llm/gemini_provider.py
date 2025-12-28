# app/services/llm/gemini_provider.py
import os
import asyncio
from typing import AsyncIterator
from google import genai

from app.services.llm.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    name = "gemini"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    async def generate(
        self,
        *,
        model: str,
        prompt: str,
    ) -> str:
        resp = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )

        if resp.text is None:
            raise RuntimeError("Gemini returned no text")

        return resp.text

    def stream(
        self,
        *,
        model: str,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        注意：
        - 這裡不是 async def
        - 回傳 AsyncIterator[str]
        """

        async def _async_stream() -> AsyncIterator[str]:
            loop = asyncio.get_running_loop()

            def sync_chunks():
                for chunk in self.client.models.generate_content_stream(
                    model=model,
                    contents=prompt,
                ):
                    if chunk.text:
                        yield chunk.text

            # 將 sync iterator 包成 async
            for text in await loop.run_in_executor(
                None, lambda: list(sync_chunks())
            ):
                yield text

        return _async_stream()
