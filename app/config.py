import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_DB = os.getenv("MYSQL_DB", "test_db")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
ROOT_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/"
NETEASE_API_URL = os.getenv("NETEASE_API_URL", "http://localhost:3000")

OPENAI_BASE_URL=os.getenv("OPENAI_BASE_URL", "https://api.siliconflow.cn/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AUDIO_ORIG_DIR = os.getenv("ORIGIN_DIR", "static/audio/orig")
AUDIO_VOC_DIR = os.getenv("VOCAL_DIR", "static/audio/voc")
AUDIO_ACC_DIR = os.getenv("ACCOMPANIMENT_DIR", "static/audio/acc")