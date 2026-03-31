from app.services.llm_adapters.openai_compatible_adapter import OpenAICompatibleAdapter


class DoubaoAdapter(OpenAICompatibleAdapter):
    """火山引擎豆包适配器
    
    使用OpenAI兼容API与豆包模型交互。
    API文档: https://www.volcengine.com/docs/82379
    """
    
    default_base_url = "https://ark.cn-beijing.volces.com/api/v3"
    provider_name = "doubao"
