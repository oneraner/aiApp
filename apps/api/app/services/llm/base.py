# app/services/llm/base.py
from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseLLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate(
        self,
        *,
        model: str,
        prompt: str,
    ) -> str:
        ...

    @abstractmethod
    def stream(
        self,
        *,
        model: str,
        prompt: str,
    ) -> AsyncIterator[str]:
        """
        注意：
        - 這裡不是 async def
        - 只規定「回傳一個 AsyncIterator」
        """
        ...
