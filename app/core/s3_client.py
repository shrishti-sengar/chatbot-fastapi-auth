# app/core/s3_client.py
import os
import logging
from botocore.exceptions import BotoCoreError, ClientError
import boto3

logger = logging.getLogger("s3_client")

# read env
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")

# create client (will use env creds or IAM role)
_s3 = boto3.client("s3", region_name=AWS_REGION)

def _format_session_text(messages):
    lines = []
    for m in messages:
        lines.append(f"User: {m['user_message']}")
        lines.append(f"AI:   {m['ai_reply']}")
        lines.append("")
    return "\n".join(lines)

def upload_session_to_s3(session_id: str, messages):
    """
    Synchronous upload helper (BackgroundTasks will call this).
    messages: list of dicts (user_message, ai_reply, created_at)
    """
    if not S3_BUCKET:
        logger.warning("S3_BUCKET not configured; skipping upload for session %s", session_id)
        return

    key = f"logs/session_{session_id}.txt"
    body = _format_session_text(messages)

    try:
        _s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body.encode("utf-8"))
        logger.info("Uploaded session %s to s3://%s/%s", session_id, S3_BUCKET, key)
    except (BotoCoreError, ClientError) as e:
        logger.exception("Failed to upload session %s to S3: %s", session_id, e)
