import os
import asyncio
import httpx
import logging

logger = logging.getLogger("openai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


async def get_ai_reply(user_message: str, max_retries: int = 3, timeout: int = 15) -> str:
    """
    Async call to OpenAI chat completions with retry/backoff.
    Returns the assistant reply string on success, raises Exception on final failure.
    """
    url = f"{OPENAI_API_BASE}/chat/completions"
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
    }

    backoff = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(url, headers=HEADERS, json=payload)
                if resp.status_code == 429:
                    # Check if it's quota vs rate-limit
                    data = resp.json()
                    err_type = data.get("error", {}).get("type")
                    logger.warning("OpenAI 429: %s", data)
                    if err_type == "insufficient_quota":
                        # no point in retrying — surface fallback
                        raise RuntimeError("insufficient_quota")
                    # else: maybe rate limit, check Retry-After
                    retry_after = int(resp.headers.get("Retry-After", 1))
                    await asyncio.sleep(retry_after)
                    continue
                resp.raise_for_status()
                data = resp.json()
                # Extract assistant message (safe checks)
                choices = data.get("choices") or []
                if not choices:
                    raise RuntimeError("No choices in OpenAI response")
                message = choices[0].get("message", {}).get("content", "")
                return message.strip()
        except RuntimeError as e:
            # bubble up for insufficient_quota so caller can fallback
            raise
        except (httpx.HTTPError, httpx.TimeoutException) as e:
            logger.exception("OpenAI call failed: %s", e)
            if attempt == max_retries:
                raise
            await asyncio.sleep(backoff)
            backoff *= 2.0
