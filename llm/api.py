import requests



def get_response(
    model, 
    api_key,
    messages, 
    temperature=1.0, 
    max_tokens=1000, 
    top_p=1.0, 
    stream=False, 
    stop=None,
    ) -> str:
    url = "https://api.f5ai.ru/v2/chat/completions"
    headers = {
        "X-Auth-Token": api_key,
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
        return response.json()["message"]["content"]
    else:
        return f"Error: {response.status_code} {response.text}"