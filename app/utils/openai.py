from openai import OpenAI
from typing import List, Dict
from app.config import OPENAI_BASE_URL, OPENAI_API_KEY

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

def call_openai(messages: List[Dict[str, str]], model: str, temperature: float = 0.7) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[OpenAI API 错误]: {e}"