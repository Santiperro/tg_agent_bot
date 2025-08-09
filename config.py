import os
from dotenv import load_dotenv


load_dotenv()


API_CONFIG = {
    "f5_api": {
        "base_url": "https://api.f5ai.ru/v2/chat/completions",
        "api_key_env": "F5AI_API_KEY",
        "default_model": "deepseek-chat",
        "max_tokens": 200,
        "temperature": 0.0,
        "top_p": 0.95,
    },
    "openai": {
        "base_url": None,
        "api_key_env": "OPENAI_KEY",
        "default_model": "gpt-4o-mini",
        "max_tokens": 200,
        "temperature": 0.0,
        "top_p": 0.95,
    },
}


class SecurityConfig:
    enable_chat_whitelist = True
    allowed_user_ids = [800006361]


class LLMConfig:
    api_config = "f5_api"
    base_url = API_CONFIG[api_config]["base_url"]
    api_key_env = os.getenv(API_CONFIG[api_config]["api_key_env"])
    default_model = API_CONFIG[api_config]["default_model"]
    max_tokens = API_CONFIG[api_config]["max_tokens"]
    temperature = API_CONFIG[api_config]["temperature"]
    top_p = API_CONFIG[api_config]["top_p"]


class Settings:
    tg_api_token = os.getenv("TG_BOT_TOKEN")
    llm_api_config = LLMConfig()
    security_config = SecurityConfig()


settings = Settings()
