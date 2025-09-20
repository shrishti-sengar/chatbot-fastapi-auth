# ---------- build stage ----------
FROM python:3.11-slim AS build
WORKDIR /app
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

# ---------- runtime stage ----------
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update \
  && apt-get install -y --no-install-recommends libpq5 \
  && rm -rf /var/lib/apt/lists/*

COPY --from=build /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

# create non-root user and ensure app dir + DB are owned by that user
RUN useradd --create-home appuser \
 && mkdir -p /app \
 && touch /app/chatbot.db \
 && chown -R appuser:appuser /app \
 && chmod 664 /app/chatbot.db

USER appuser



ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

# copy entrypoint into image and make executable
# copy entrypoint and set executable bit during copy (requires BuildKit / recent Docker)
COPY --chmod=0755 entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-connections", "100", \
     "--timeout", "120", "--log-level", "info"]
