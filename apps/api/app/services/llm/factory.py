# app/services/llm/factory.py
from typing import List
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.gemini_provider import GeminiProvider
from app.api.v1.models.schemas import ModelInfo

# 工廠方法：回傳所有 provider 的實例
def get_providers() -> List:
    providers = []
    try:
        providers.append(OpenAIProvider())
    except Exception:
        pass  # 如果沒有設定 API key 或初始化失敗就跳過
    try:
        providers.append(GeminiProvider())
    except Exception:
        pass
    return providers

# 統一回傳平台所有模型資訊
async def get_all_models() -> List[ModelInfo]:
    models: List[ModelInfo] = []
    for provider in get_providers():
        try:
            # list_models() 預設回傳 List[str] 或 List[dict]
            provider_models = provider.list_models()
            for m in provider_models:
                # 統一格式
                if isinstance(m, str):
                    models.append(ModelInfo(name=m, provider=provider.__class__.__name__, capabilities=[]))
                elif isinstance(m, dict):
                    models.append(ModelInfo(
                        name=m.get("name", ""),
                        provider=provider.__class__.__name__,
                        capabilities=m.get("capabilities", [])
                    ))
        except Exception:
            continue
    return models
