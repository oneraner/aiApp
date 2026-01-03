# app/services/llm/base.py
from abc import ABC, abstractmethod
from typing import AsyncIterator, List


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
    
    def list_models(self) -> List[str]:
        """
        返回此 provider 支援的模型列表
        子類別應該覆寫此方法
        """
        return []
