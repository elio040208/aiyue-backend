import re
import json
import requests
from app.config import NETEASE_API_URL
from app.utils.openai import call_openai
from app.schemas.music import RewriteLyricRequest
   
def parse_lyric(lyric: str):
    pattern = r"\[(\d{2}:\d{2}\.\d{2})\](.*)"
    lines = lyric.strip().splitlines()
    result = []

    for line in lines:
        match = re.match(pattern, line)
        if match:
            time, text = match.groups()
            result.append({"time": time, "text": text.strip()})
    return result

def get_audio_url(source_id: int) -> str:
    try:
        res = requests.get(f"{NETEASE_API_URL}/song/url", params={"id": source_id})
        res.raise_for_status()
        data = res.json()
        return data.get("data", [{}])[0].get("url") or ""
    except Exception as e:
        print(f"获取歌曲 {source_id} 播放地址失败：{e}")
        return ""

def download_audio(url: str, save_path: str) -> bool:
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载音频失败：{e}")
        return False

def get_lyric(source_id: int) -> str:
    try:
        res = requests.get(f"{NETEASE_API_URL}/lyric", params={"id": source_id})
        res.raise_for_status()
        data = res.json()
        lyric = data.get("lrc", {}).get("lyric", "")
        return parse_lyric(lyric)
    except Exception as e:
        print(f"获取歌词失败: {e}")
        return None

def rewrite_lyric(request: RewriteLyricRequest):
    lyric_str = json.dumps([line.model_dump() for line in request.lyric], ensure_ascii=False, indent=2)

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个歌词改写助手。用户输入的是 JSON 格式的歌词，每项包含 `time` 和 `text`。\n"
                "你需要根据用户的改写要求，仅修改每一项的 `text` 内容。\n"
                "注意：只能返回结构相同的 JSON 格式，不要添加任何解释说明。\n"
                "不能更改时间戳 `time`。\n"
                "请确保返回的是纯 JSON 数组结构。"
            )
        },
        {
            "role": "user",
            "content": (
                f"请将下面这段歌词改写：{request.instruction}\n\n"
                f"原始歌词：\n{lyric_str}"
            )
        }
    ]

    response = call_openai(messages, model="Qwen/Qwen3-8B", temperature=0.7)
    
    try:
        return json.loads(response)
    except Exception as e:
        raise ValueError(f"模型返回无法解析为 JSON：{e}\n原始输出：\n{response}")