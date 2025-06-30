import openai
from typing import List, Dict
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_openai(messages: List[Dict[str, str]], model: str, temperature: float = 0.7) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[OpenAI API 错误]: {e}")