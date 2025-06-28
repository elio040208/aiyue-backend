import requests
from app.config import NETEASE_API_URL

def get_audio_url(song_id: int) -> str:
    try:
        res = requests.get(f"{NETEASE_API_URL}/song/url", params={"id": song_id})
        res.raise_for_status()
        data = res.json()
        return data.get("data", [{}])[0].get("url") or ""
    except Exception as e:
        print(f"获取歌曲 {song_id} 播放地址失败：{e}")
        return ""