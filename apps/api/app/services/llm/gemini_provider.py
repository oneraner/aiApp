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
        Generate streaming response from Gemini API.
        Limited to 500 output tokens to prevent quota abuse.
        """
        try:
            # Configure generation with token limit
            generation_config = {
                "max_output_tokens": 500,  # Hard limit to prevent abuse
                "temperature": 0.7,
            }
            
            response = await self.client.models.generate_content(
                model=model, # The model name from list_models already includes "gemini-", so no need for "models/" prefix here.
                contents=prompt,
                generation_config=generation_config,
                stream=True
            )
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            error_msg = str(e)
            print(f"[Gemini Error] {error_msg}")
            # Depending on the desired behavior, you might want to re-raise,
            # yield an error message, or just let the stream end.
            # For now, we'll just print and let the stream end.
    
    def list_models(self):
        """
        從 Google API 動態取得可用的 Gemini 模型列表
        """
        try:
            # 使用 Gemini client 列出所有可用模型
            models_response = self.client.models.list()
            
            # 過濾出 gemini 模型並提取名稱
            gemini_models = []
            for model in models_response:
                model_name = model.name
                # 只保留 gemini 開頭的模型，並去掉 "models/" 前綴
                if "gemini" in model_name.lower():
                    # 格式化模型名稱（去掉 "models/" 前綴）
                    clean_name = model_name.replace("models/", "")
                    gemini_models.append(clean_name)
            
            return sorted(gemini_models) if gemini_models else []
        except Exception as e:
            # 如果 API 調用失敗，返回預設的模型列表
            print(f"Warning: Failed to fetch models from Gemini API: {e}")
            return [
                "gemini-2.0-flash-exp",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b",
            ]
