from app.services.llm_adapters.openai_compatible_adapter import OpenAICompatibleAdapter


class QwenAdapter(OpenAICompatibleAdapter):
    """通义千问适配器
    
    使用OpenAI兼容API与通义千问模型交互。
    API文档: https://help.aliyun.com/zh/dashscope/developer-reference/api-details
    """
    
    default_base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    provider_name = "qwen"
