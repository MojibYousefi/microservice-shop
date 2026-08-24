FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY backend/gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/config /app/backend/config
COPY backend/gateway /app/backend/gateway
COPY frontend /app/frontend

EXPOSE 8000

CMD ["python", "-m", "backend.gateway.main"]
