from app.services.llm_adapters.openai_compatible_adapter import OpenAICompatibleAdapter


class GLMAdapter(OpenAICompatibleAdapter):
    """智谱GLM适配器
    
    使用OpenAI兼容API与智谱GLM模型交互。
    API文档: https://open.bigmodel.cn/dev/api
    """
    
    default_base_url = "https://open.bigmodel.cn/api/paas/v4"
    provider_name = "glm"
