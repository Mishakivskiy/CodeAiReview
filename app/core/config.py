import os
from dotenv import load_dotenv

load_dotenv()


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
github_base_url = "https://api.github.com"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
