# app/services/llm/openai_provider.py
import os
import asyncio
from typing import AsyncIterator
from openai import OpenAI

from app.services.llm.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    name = "openai"

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    async def generate(
        self,
        *,
        model: str,
        prompt: str,
    ) -> str:
        response = self.client.responses.create(
            model=model,
            input=prompt,
        )
        return response.output_text

    def stream(
        self,
        *,
        model: str,
        prompt: str,
    ) -> AsyncIterator[str]:

        async def _async_stream() -> AsyncIterator[str]:
            loop = asyncio.get_running_loop()

            def sync_events():
                with self.client.responses.stream(
                    model=model,
                    input=prompt,
                ) as stream:
                    for event in stream:
                        if event.type == "response.output_text.delta":
                            yield event.delta

            for chunk in await loop.run_in_executor(
                None, lambda: list(sync_events())
            ):
                yield chunk

        return _async_stream()
