from app.services.llm_adapters.openai_compatible_adapter import OpenAICompatibleAdapter


class KimiAdapter(OpenAICompatibleAdapter):
    """Moonshot Kimi适配器
    
    使用OpenAI兼容API与Kimi模型交互。
    API文档: https://platform.moonshot.cn/docs
    """
    
    default_base_url = "https://api.moonshot.cn/v1"
    provider_name = "kimi"
