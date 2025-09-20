
import os, asyncio, httpx
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
url = f"{OPENAI_API_BASE}/chat/completions"
headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"}
payload = {"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"hello"}],"max_tokens":50}
async def run():
    async with httpx.AsyncClient() as c:
        r = await c.post(url, headers=headers, json=payload)
        print("status:", r.status_code)
        try:
            print("body:", r.json())
        except Exception:
            print("raw:", r.text)
asyncio.run(run())
