import requests
from app.database import SessionLocal
from app.models import Song

NETEASE_API_URL = "http://localhost:3000"
HOT_PLAYLIST_ID = 3778678

def main():
    db = SessionLocal()
    try:
        print("开始抓取网易云热歌榜歌曲信息...")
        res = requests.get(f"{NETEASE_API_URL}/playlist/detail", params={"id": HOT_PLAYLIST_ID})
        res.raise_for_status()
        data = res.json()
        tracks = data.get("playlist", {}).get("tracks", [])
        print(f"共获取到 {len(tracks)} 首歌曲")

        added = 0
        for track in tracks:
            source_id = str(track["id"])
            exists = db.query(Song).filter_by(source_id=source_id).first()
            if exists:
                continue

            song = Song(
                source_id=source_id,
                platform="netease",
                title=track.get("name", ""),
                artist=", ".join([a["name"] for a in track.get("ar", [])]),
                album=track.get("al", {}).get("name", ""),
                cover_url=track.get("al", {}).get("picUrl", ""),
                duration=track.get("dt", 0) // 1000,
            )
            db.add(song)
            added += 1

        db.commit()
        print(f"成功同步 {added} 首歌曲到数据库")
    except Exception as e:
        print(f"程序异常退出: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
