import requests

from config import settings
from bot.exceptions import LLMApiError


def get_response(
    model, 
    messages, 
    temperature=1.0, 
    max_tokens=10000, 
    top_p=1.0, 
    stream=False, 
    stop=None,
    ) -> str:
    url = settings.llm_api_config.base_url
    headers = {
        "X-Auth-Token": settings.llm_api_config.api_key_env,
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "stream": stream,
        "stop": stop,
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        elif "message" in response_data:
            return response_data["message"]["content"]
        else:
            raise LLMApiError("Unexpected response format")
    else:
        try:
            error_data = response.json()
            if "error" in error_data and "message" in error_data["error"]:
                error_message = error_data["error"]["message"]
                raise LLMApiError(f"API Error: {error_message}")
            else:
                raise LLMApiError(f"HTTP {response.status_code}: {response.text}")
        except requests.exceptions.JSONDecodeError:
            raise LLMApiError(f"HTTP {response.status_code}: {response.text}")